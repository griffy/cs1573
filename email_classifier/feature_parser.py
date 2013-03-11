import re

class FeatureParser(object):
    """
    Class that will be used to set up the feature vector
    
    Arguments (for constructor):
        user_folder_uri       :-  Path to folder representing a user in the dataset

    Goal:
        Return a matrix of of the form |class|feature1|feature2|...|
                                       |...  | ...    | ...    |...|

    """

    def __init__(self, user_folder_uri, word_list):
        self.user_folder_uri = user_folder_uri
        self.global_names = dict()

    def get_feature_matrix(self, classification_folder):
        """
            Returns a list of feature vectors representing the emails
            contained within the specified classification folder
        """
        feature_matrix = []
        for root, dirs, emails in os.walk(os.path.join(self.user_folder_uri, 
                                                       classification_folder)):
            for email in emails:
                email_uri = os.path.join(classification_folder, email)
                names, secondary_names, body_text = self.get_mail_elements(email_uri)

                # TODO: strip out unhelpful words from body_text 
                #       by using chi-square / info gain

                self.data_set.append()

    def parse(self, email):
        """
            Returns a vector representation of an email
        """


    def initialize_matrix(self):
        """
        """
        self.data_set = []

        for root, dirs, emails in os.walk(os.path.join(self.user_folder_uri, 
                                                       self.classification_folder)):
            for email in emails:
                names, secondary_names, body_text = self.get_mail_elements(email)
                self.data_set.append()
        for d in self.data_set:
            for n in d[4]:
                if n in self.global_names:
                   self.global_names[n] += 1
                else:
                    self.global_names[n] = 1
            for n in d[5]:
                if n in self.global_names:
                    self.global_names[n] += 1
                else:
                    self.global_names[n] = 1

    def print_data_set(self):
        """
        For testing purposes
        """
        for d in self.raw_data_set:
            print d

    def print_global_names(self):
        """
        For testing purposes. Prints out all names mentioned in to, from, cc, and bcc
        of all emails
        """
        # How many times must a name appear for it to matter as a feature?
        for k in self.global_names.keys():
            if self.global_names[k] > 3:
                print str(k)  + '  :-  ' + str(self.global_names[k])

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


            if hour in range(9, 18):
                return 'work'
            elif hour in range(18, 22):
                return 'evening'
            elif hour in range(22, 25) or hour in range(0, 6):
                return 'night'
            elif hour in range(6, 9):
                return 'morning'
        else:
            print "Hour not found!"
            raise ValueError