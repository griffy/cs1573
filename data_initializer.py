class DataInitializer(object):
    """
    Class that will be used to set up the feature vector.
    
    Arguments (for constructor):
        data_set     :-      List of tuples passed from driver.py
                             [(classification1, path1), (classification2, path2),...]
    Important Methods:

    Goal:
        Return a matrix of of the form |class|feature1|feature2|...|
                                       |...  | ...    | ...    |...|

    """
    
    def __init__(self, data_set):
        """
        Retrieves the data set whose features matrix will be set up
        """
        self.data_set = data_set
        

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


    def initialize_names_list(self):
        """
        Builds a list all the names in a users mailbox to check against
        """
        pass

    def parse_names(self, document):
        """
        Parses document for names found in names_list
        """
        pass

    def parse_time_of_day(self, document):
        pass

    def parse_month(self, document):
        pass

    def chi_square(self):
        pass

    def information_gain(self):
        pass
