
import sys
import os
import re

class DataInitializer(object):
    """
    Class that will be used to set up the feature vector.
    
    Arguments (for constructor):
        folder_name     :-      String that is to regexp match one of the enron
                                folders (defaults to beck)
    Methods:
        initialize_mapping()    :-      Prints to stdout   <class> <file-path>
                                        Fills   class_document_map dictionary
    """
    
    def __init__(self, folder_name = 'beck'):
        """
        Given folder_name, supplies data_path, which contains the relative path
        to that users email folders.
        Wanted to do fuzzy matching because Rishi is forgetful
        """
        self.data_path = ''
        self.class_document_map = dict()
        
        reg_obj = re.compile(".*" + folder_name + ".*", re.IGNORECASE)
        if reg_obj.search("beck-s"):
            self.data_path = "data/beck-s/"
        elif reg_obj.search("former-d"):
            self.data_path = "data/former-d/" 
        elif reg_obj.search("kaminski-v"):
            self.data_path = "data/kaminski-v/" 
        elif reg_obj.search("kitchen-l"):
            self.data_path = "data/kitchen-l/" 
        elif reg_obj.search("lokay-m"):
            self.data_path = "data/lokay-m/" 
        elif reg_obj.search("sanders-r"):
            self.data_path = "data/sanders-r/" 
        elif reg_obj.search("williams-w3"):
            self.data_path = "data/williams-w3/"

    def initialize_mapping(self):
        """
        Fills class_document_map   :-
               class_document_map['classname'] = [emailpath_1, ..., emailpath_n]
               Going to need this later for doq_freq()
        """
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), self.data_path)):
            for f in files:
                if str(os.path.split(root)[1]) in self.class_document_map:
                    self.class_document_map[str(os.path.split(root)[1])].append(str(os.path.join(root, f)))
                else:
                    self.class_document_map[str(os.path.split(root)[1])] = []
                    self.class_document_map[str(os.path.split(root)[1])].append(str(os.path.join(root, f)))
                sys.stdout.write(str(os.path.split(root)[1]) + "\t" + \
                                     str(os.path.join(root, f)) + "\n")

    def print_class_document_map(self):
        """
        For testing purposes.
        Just prints out the mapping between classifications and their emails.
        (self.class_document_map)
        """
        for k in di.class_document_map:
            print str(k) + " : " + str(di.class_document_map[k])

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
