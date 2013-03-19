import re
import os
import math
from email import Email

def get_emails(user_folder_uri):
    """
        Returns a list of all the emails inside the given user folder
    """
    emails = []
    for classification_folder in os.listdir(user_folder_uri):
        for root, dirs, files in os.walk(os.path.join(user_folder_uri, 
                                                      classification_folder)):
            for f in files:
                email_uri = os.path.join(user_folder_uri, classification_folder, f)
                email = Email(email_uri)
                emails.append(email)
    return emails

def get_word_counts(emails):
    """
        Looks at all emails and creates two dictionaries: one containing
        the count of all words per classification, and the other containing 
        the count of all words over the entire dataset
    """
    global_word_count = {}
    class_word_count = {}

    for email in emails:
        if email.classification not in class_word_count:
            class_word_count[email.classification] = {}

        for word in email.get_words():
            if word not in global_word_count:
                global_word_count[word] = 1
            else:
                global_word_count[word] += 1

            if word not in class_word_count[email.classification]:
                class_word_count[email.classification][word] = 1
            else:
                class_word_count[email.classification][word] += 1

    return global_word_count, class_word_count

def get_name_counts(emails):
    """
        Looks at all emails and creates two dictionaries: one containing
        the count of all names per classification, and the other containing 
        the count of all names over the entire dataset
    """
    global_name_count = {}
    class_name_count = {}

    for email in emails:
        if email.classification not in class_name_count:
            class_name_count[email.classification] = {}

        for name in email.get_names():
            if name not in global_name_count:
                global_name_count[name] = 1
            else:
                global_name_count[name] += 1

            if name not in class_name_count[email.classification]:
                class_name_count[email.classification][name] = 1
            else:
                class_name_count[email.classification][name] += 1

    return global_name_count, class_name_count

def create_feature_sets(emails):
    """ 
        Given a list of emails, returns two sets of features: words and names
    """
    global_word_count, class_word_count = get_word_counts(emails)
    global_name_count, class_name_count = get_name_counts(emails)

    word_features = set()
    name_features = set()

    for word in global_word_count.keys():
        word_features.add(word)

    # TODO: How many times must a name appear for it to matter as a feature?
    for name in global_name_count.keys():
        name_features.add(name)

    # make the sets immutable now
    return frozenset(word_features), frozenset(name_features)

def reduce_feature_sets(word_features, name_features, emails, using='information gain'):
    """
        Uses information gain / chi-square to narrow down the word and name features
    """
    if using == 'information gain':
        word_features, name_features = reduce_by_information_gain(word_features, name_features, emails)
    elif using == 'chi square':
        word_features, name_features = reduce_by_chi_square(word_features, name_features, emails)
    return word_features, name_features

def reduce_by_information_gain(word_features, name_features, emails):
    new_word_features = set(word_features)
    new_name_features = set(name_features)

    # TODO: info gain

    # make the new sets immutable
    return frozenset(new_word_features), frozenset(new_name_features)

def reduce_by_chi_square(word_features, name_features, emails):
    new_word_features = set(word_features)
    new_name_features = set(name_features)

    # TODO: chi square

    # make the new sets immutable
    return frozenset(new_word_features), frozenset(new_name_features)

def extract_feature_sets(emails, using='information gain'):
    """
        Given a list of emails, extracts two sets of features from them: words and names

        The word and name feature sets are reduced using the strategy provided as the
        'using' argument.
    """
    word_features, name_features = create_feature_sets(emails)
    word_features, name_features = reduce_feature_sets(word_features, name_features, emails, using)
    return word_features, name_features

class ExampleType(object):
    """
        A factory for generating examples that all fit a certain profile, i.e. have
        the same input vectors and possible classifications.

        Essentially, it is a class for holding metadata about examples.
    """
    def __init__(self, classifications, features):
        self.classifications = classifications
        self.features = features
        self.feature_lookup = {}
        for index, feature in enumerate(self.features):
            self.feature_lookup[feature] = index

    def get_index(self, feature):
        return self.feature_lookup[feature]

    def create_example(self, id, input_vector, output):
        return Example(self, id, input_vector, output)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str([feature.name for feature in self.features])

class Example(object):
    """
        An instance from a dataset, associated with an ExampleType
    """
    def __init__(self, type, id, input_vector, output):
        self.type = type
        self.id = id
        self.input_vector = input_vector
        self.output = output

    def get_value(self, feature):
        feature_index = self.type.get_index(feature)
        if 0 <= feature_index < len(self.input_vector):
            return self.input_vector[feature_index]
        return None

    def __repr__(self):
        return str(self)

    def __str__(self):
        rep = "%s,%s" % (self.id, self.output)
        for feature_value in self.input_vector:
            rep += ",%s" % feature_value
        return rep

class DataInitializer(object):
    """
        Class that will be used to set up the feature vector on a per-user basis
        
        Arguments (for constructor):
            user_folder_uri       :-  Path to folder representing a user in the dataset
            reduce_using          :-  Strategy for reducing feature sets

        Goal:
            Return a matrix of of the form |class|feature1|feature2|...|
                                           |...  | ...    | ...    |...|

            It now returns a list of examples, which are themselves representations of
            the above form. So, a matrix + the overhead of many, many objects.

    """
    def __init__(self, user_folder_uri, reduce_using='information gain'):
        self.user_folder_uri = user_folder_uri
        # load the emails in the user's folder
        self.emails = get_emails(user_folder_uri)
        # pull out the (term) features we are interested in from the dataset
        word_features, name_features = extract_feature_sets(self.emails, reduce_using)
        self.word_features = word_features
        self.name_features = name_features

    def get_example_type(self):
        classifications = os.listdir(self.user_folder_uri)
        # give 'special' features __ pre and postfixes to avoid conflict
        # with word features
        features = ['__month__', '__time-of-day__']
        for name_feature in self.name_features:
            features.append('__name__' + name_feature)
        for word_feature in self.word_features:
            features.append(word_feature)
        return ExampleType(classifications, features)

    def preprocess(self):
        """
            Constructs an Example (input vector + output) for each email and returns:
                ExampleType, (List of) Examples
        """
        # build up the metadata for each example
        example_type = self.get_example_type()

        # for each email, create an example
        examples = []
        for email in self.emails:
            examples.append(self._parse_email(email, example_type))

        return example_type, examples

    def _parse_email(self, email, example_type):
        """
            Returns an Example representing the given email
        """
        # FIXME: not a fan of this method or its hard-coded assumptions

        input_vector = []
        input_vector.append(email.get_month())
        input_vector.append(email.get_time_of_day())
        for index in range(2, len(example_type.features)):
            feature = example_type.features[index]
            if feature.startswith('__name__'):
                name_occurs = feature[len('__name__'):] in email.get_names()
                input_vector.append(name_occurs)
            else:
                input_vector.append(self._tf_idf(feature, email, email.classification))

        return example_type.create_example(email.uri, input_vector, email.classification)

    def _tf_idf(self, word, document, classification):
        """
            Computes the tf-idf value for a
            'word' in training example 'document' with classification 'classification'
        """
        return self._term_freq(word, document) * self._inverse_doc_freq(word, classification)

    def _term_freq(self, word, document):
        """
            (number_of_times_word_appears_in_document)
            divided by
            (max_number_of_times_any_word_appears_in_document)
        """
        return document.count(word) / document.max_word_frequency(self.word_features)

    def _inverse_doc_freq(self, word, classification):
        """
            log( (num_docs_in_classification) / (1 + num_docs_with_word_in_it_in_classification) )
        """
        num_docs = 0
        num_docs_with_word = 0
        for email in self.emails:
            if email.classification == classification:
                num_docs += 1
                if email.count(word) > 0:
                    num_docs_with_word += 1
        return math.log(num_docs / (1 + num_docs_with_word))
