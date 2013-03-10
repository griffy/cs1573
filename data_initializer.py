import re

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
        for d in self.data_set:
            (n, s, b) = self.get_mail_elements(d[1])
            d.append(n)
            d.append(s)
            d.append(b)

    def print_data_set(self):
        for d in self.data_set:
#            print d
            print d[:-1]

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

    def clean_contact(self, name_string):
        """
        The names in the 'to, from, cc, bcc' sections of an email are often very muddy.
        This is an attempt to normalize them to an extent.
         - Sometimes its <name> <address>, <n2> <a2>,...  :-  just want names
         - Sometimes of the form   first.last@company  :- just want first last
        """
        name_regex_obj = re.compile("(.*)<")
        at_regex_obj = re.compile("(.)@")
        name_groups = name_regex_obj.search(name_string)
        if name_groups:
            name_string = name_groups.group(1)
        at_groups = at_regex_obj.search(name_string)
        if at_groups:
            name_string = name_string.split('@')[0]
        name_string = name_string.replace('.', ' ')
        return name_string.strip()
        

    def get_mail_elements(self, document_address):
        """
        This method is meant to abstract an email in to objects we can parse.
        Two sets of words for names and a long string for the body.
        ARGUMENTS
                document_address :- The full path to the email we are parsing
        RETURNS
                (names, secondary_names, body_text)
                        names           :- Set of names found in the To and From sections.
                        secondary_names :- Set of names found in the cc and bcc sections.
                        body_text       :- Long string that represents the body.
        """
        f = open(document_address)
        names = set()
        secondary_names = set()
        body_found = False
        body_text = ''
        to_regex_obj   = re.compile("^X-To:.*")
        cc_regex_obj   = re.compile("^X-cc:.*")
        bcc_regex_obj  = re.compile("^X-bcc:.*")
        body_regex_obj = re.compile("^X-FileName:.*")
        from_regex_obj = re.compile("^X-From:.*")
        
        lines = f.readlines()
        for line in lines:
            if body_found:
                body_text += line.strip() + " "
                continue
            if from_regex_obj.search(line):
                line = line[len("X-From:"):]
                for elt in line.split(","):
                    elt = self.clean_contact(elt)
                    if elt != '':
                        names.add(elt.strip())
            elif to_regex_obj.search(line):
                line = line[len("X-To:"):]
                for elt in line.split(","):
                    elt = self.clean_contact(elt)
                    if elt != '':
                        names.add(elt.strip())
            elif cc_regex_obj.search(line):
                line = line[len("X-cc:"):]
                for elt in line.split(","):
                    elt = self.clean_contact(elt)
                    if elt != '':
                        secondary_names.add(elt.strip())
            elif bcc_regex_obj.search(line):
                line = line[len("X-bcc:"):]
                for elt in line.split(","):
                    elt = self.clean_contact(elt)
                    if elt != '':
                        secondary_names.add(elt.strip())
            elif body_regex_obj.search(line):
                body_found = True
        f.close()
        return (names, secondary_names, body_text.strip())
