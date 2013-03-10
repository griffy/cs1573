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
            (tod, m, n, s, ss, b) = self.get_mail_elements(d[1])
            d.append(tod)
            d.append(m)
            d.append(n)
            d.append(s)
            d.append(ss)
            d.append(b)

    def print_data_set(self):
        for d in self.data_set:
            print d

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

    def parse_time_of_day(self, date):
        tod_regex_obj = re.compile(r'.*(\d{2}):\d{2}:\d{2}.*')
        hours_obj = tod_regex_obj.search(date)
        hour = -1
        if hours_obj:
            hour = int(hours_obj.groups(1)[0])
            if hour in range(9, 18):
                return 'work'
            elif hour in range(18, 22):
                return 'evening'
            elif hour in range(22, 25) or hour in range(0, 6):
                return 'night'
            elif hour in range(6, 10):
                return 'morning'
        else:
            print "Hour not found!"
            raise ValueError
    

    def parse_month(self, date):
        if re.search('Jan', date, re.IGNORECASE):
            return 'Jan'
        elif re.search('Feb', date, re.IGNORECASE):
            return 'Feb'
        elif re.search('Mar', date, re.IGNORECASE):
            return 'Mar'
        elif re.search('Apr', date, re.IGNORECASE):
            return 'Apr'
        elif re.search('May', date, re.IGNORECASE):
            return 'May'
        elif re.search('Jun', date, re.IGNORECASE):
            return 'Jun'
        elif re.search('Jul', date, re.IGNORECASE):
            return 'Jul'
        elif re.search('Aug', date, re.IGNORECASE):
            return 'Aug'
        elif re.search('Sep', date, re.IGNORECASE):
            return 'Sep'
        elif re.search('Nov', date, re.IGNORECASE):
            return 'Nov'
        elif re.search('Oct', date, re.IGNORECASE):
            return 'Oct'
        elif re.search('Dec', date, re.IGNORECASE):
            return 'Dec'
        else:
            print "Month not present"
            raise ValueError

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
        subject_text = ''
        month = ''
        time_of_day = ''
        to_regex_obj   = re.compile("^X-To:.*")
        cc_regex_obj   = re.compile("^X-cc:.*")
        bcc_regex_obj  = re.compile("^X-bcc:.*")
        body_regex_obj = re.compile("^X-FileName:.*")
        from_regex_obj = re.compile("^X-From:.*")
        date_regex_obj = re.compile("^Date:.*")        
        subject_regex_obj = re.compile("^Subject:.*")
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
            elif date_regex_obj.search(line):
                month = self.parse_month(line)
                time_of_day = self.parse_time_of_day(line)
            elif subject_regex_obj.search(line):
                subject_text = line[len("Subject:"):]
            elif body_regex_obj.search(line):
                body_found = True
        f.close()
        return (time_of_day, month, names, secondary_names, subject_text.strip(), body_text.strip())
