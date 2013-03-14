import re
from email import Email

class FeatureParser(object):
    """
    Class that will be used to set up the feature vector
    
    Arguments (for constructor):
        user_folder_uri       :-  Path to folder representing a user in the dataset

    Goal:
        Return a matrix of of the form |class|feature1|feature2|...|
                                       |...  | ...    | ...    |...|

    """

    def __init__(self, user_folder_uri):
        self.user_folder_uri = user_folder_uri

        self.load_emails()

        self.collect_words()
        self.collect_names()

        self.prepare_features()

    def load_emails(self):
        """
            Loads the user's emails into an array we can manipulate in future methods

            This may be a terrible idea; we'll see!
        """
        self.emails = []
        for classification_folder in os.listdir(self.user_folder_uri):
            for root, dirs, files in os.walk(os.path.join(self.user_folder_uri, 
                                                          classification_folder)):
                for f in files:
                    email_uri = os.path.join(self.user_folder_uri, classification_folder, f)
                    email = Email(email_uri)
                    self.emails.append(email)

    def collect_words(self):
        """
            Looks at all emails in all classification folders and compiles 
            a dictionary containing the count of all words appearing in them
        """
        self.global_word_count = {}
        self.class_word_count = {}
        for email in self.emails:
            if email.classification not in self.class_word_count:
                self.class_word_count[email.classification] = {}

            for word in email.get_words():
                if word not in self.global_word_count:
                    self.global_word_count[word] = 1
                else:
                    self.global_word_count[word] += 1

                if word not in self.class_word_count[email.classification]:
                    self.class_word_count[email.classification][word] = 1
                else:
                    self.class_word_count[email.classification][word] += 1

    def collect_names(self):
        """
            Looks at all emails in all classification folders and compiles 
            a dictionary containing the count of all names appearing in them
        """
        self.global_name_count = {}
        self.class_name_count = {}
        for email in self.emails:
            if email.classification not in self.class_name_count:
                self.class_name_count[email.classification] = {}

            for name in email.get_receiver_names():
                if name not in self.global_name_count:
                    self.global_name_count[name] = 1
                else:
                    self.global_name_count[name] += 1

                if name not in self.class_name_count[email.classification]:
                    self.class_name_count[email.classification][name] = 1
                else:
                    self.class_name_count[email.classification][name] += 1

    def prepare_features(self):
        """
            TODO: Uses information gain / chi-square to narrow down the word and name features
        """
        self.word_features = set()
        self.name_features = set()

        for word in self.global_word_count.keys():
            self.word_features.add(word)

        for name in self.global_name_count.keys():
            self.name_features.add(name)


    def get_feature_matrix(self):
        """
            Returns a list of feature dictionaries representing the emails in the user folder
        """
        feature_matrix = []
        for email in self.emails:
            feature_matrix.append(self.parse_features(email))
        return feature_matrix

    def parse_features(self, email):
        """
            Returns a feature representation of an email
        """
        features = {'month': '', 'time-of-day': '', 'words': {}, 'names': {}}

        features['month'] = email.get_month()
        features['time-of-day'] = email.get_time_of_day()
        for word_feature in self.word_features:
            features['words'][word_feature] = self.tf_idf(word_feature, email, email.classification)
        for name_feature in self.name_features:
            features['names'][name_feature] = name_feature in email.get_receiver_names()

        return features

    def print_global_names(self):
        """
        For testing purposes. Prints out all names mentioned in to, from, cc, and bcc
        of all emails
        """
        # How many times must a name appear for it to matter as a feature?
        for k in self.global_name_count.keys():
            if self.global_name_count[k] > 3:
                print str(k)  + '  :-  ' + str(self.global_name_count[k])

    def tf_idf(self, word, document, classification):
        """
        Computes the tf-idf value for a
        'word' in training example 'document' with clasification 'classification'
        """
        return term_freq(word, document) * doc_freq(word, classification)

    def term_freq(self, word, document):
        """
        (number_of_times_word_appears_in_document)
        divided by
        (max_number_of_times_any_word_appears_in_document)
        """
        pass

    def doc_freq(self, word, classification):
        """
        log( (num_docs_in_classification) / (1 + num_docs_with_word_in_it_in_classification) )
        """
        pass

    def chi_square(self):
        pass

    def information_gain(self):
        pass


