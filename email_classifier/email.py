import re

to_regex_obj = re.compile("^X-To:.*")
cc_regex_obj = re.compile("^X-cc:.*")
bcc_regex_obj = re.compile("^X-bcc:.*")
body_regex_obj = re.compile("^X-FileName:.*")
from_regex_obj = re.compile("^X-From:.*")
date_regex_obj = re.compile("^Date:.*")        
subject_regex_obj = re.compile("^Subject:.*")

tod_regex_obj = re.compile(r'.*(\d{2}):\d{2}:\d{2}.*')

name_regex_obj = re.compile("(.*)<")
at_regex_obj = re.compile("(.)@")

def parse_email(uri):
    """ 
        Takes a URI to a file containing an email and returns
        a tuple containing the following attributes:
            (datetime, from, to, cc, bcc, subject, body)
    """

    datetime = ''
    header_from = ''
    header_to = ''
    header_cc = ''
    header_bcc = ''
    subject = ''
    body = ''

    with open(uri, 'r') as email:
        body_found = False
        lines = email.readlines()
        for line in lines:
            if body_found:
                # skip the first empty line
                if body or line.strip():
                    body += line
                continue
            if from_regex_obj.search(line):
                header_from = line[len("X-From:"):].strip()
            elif to_regex_obj.search(line):
                header_to = line[len("X-To:"):].strip()
            elif cc_regex_obj.search(line):
                header_cc = line[len("X-cc:"):].strip()
            elif bcc_regex_obj.search(line):
                header_bcc = line[len("X-bcc:"):].strip()
            elif date_regex_obj.search(line):
                datetime = line[len("Date:"):].strip()
            elif subject_regex_obj.search(line):
                subject = line[len("Subject:"):].strip()
            elif body_regex_obj.search(line):
                body_found = True
    return (datetime, header_from, header_to, header_cc, header_bcc, subject, body)

class Email(object):
    """ 
        Given a URI to an email file, parses its contents and stores
        relevant information as attributes
    """
    def __init__(self, uri):
        self.uri = uri

        fields = parse_email(uri)

        self.datetime = fields[0]
        self.header_from = fields[1]
        self.header_to = fields[2]
        self.header_cc = fields[3]
        self.header_bcc = fields[4]
        self.subject = fields[5]
        self.body = fields[6]

    def _extract_name(self, contact):
        """
            The names in the 'to, from, cc, bcc' sections of an email are often very muddy.
            This is an attempt to normalize them to an extent.
             - Sometimes its <name> <address>, <n2> <a2>,...  :-  just want names
             - Sometimes of the form   first.last@company  :- just want first last
        """
        name_groups = name_regex_obj.search(contact)
        if name_groups:
            contact = name_groups.group(1)
        at_groups = at_regex_obj.search(contact)
        if at_groups:
            contact = contact.split('@')[0]
        contact = contact.replace('.', ' ')
        contact = contact.replace('\"', '')
        return contact.strip()

    def _extract_names(self, header_field):
        """
            Given a header field (string), returns a list of the real names contained within
        """
        names = []
        for contact in header_field.split(','):
            name = self._extract_name(contact)
            if name:
                names.append(name)
        return names

    def get_from_names(self):
        """
            Returns a list of names found in the X-From field
        """
        return self._extract_names(self.header_from)

    def get_to_names(self):
        """
            Returns a list of names found in the X-To field
        """
        return self._extract_names(self.header_to)

    def get_cc_names(self):
        """
            Returns a list of names found in the X-cc field
        """
        return self._extract_names(self.header_cc)

    def get_bcc_names(self):
        """
            Returns a list of names found in the X-bcc field
        """
        return self._extract_names(self.header_bcc)

    def get_hour(self):
        """
            Returns the hour the email was received (0..24)
        """
        hours_obj = tod_regex_obj.search(self.datetime)
        if hours_obj:
            return int(hours_obj.groups(1)[0])
        raise ValueError("Hour not found")
    
    def get_month(self):
        """
            Returns the month the email was received as a three-letter abbreviation
        """
        if re.search('Jan', self.datetime, re.IGNORECASE):
            return 'Jan'
        elif re.search('Feb', self.datetime, re.IGNORECASE):
            return 'Feb'
        elif re.search('Mar', self.datetime, re.IGNORECASE):
            return 'Mar'
        elif re.search('Apr', self.datetime, re.IGNORECASE):
            return 'Apr'
        elif re.search('May', self.datetime, re.IGNORECASE):
            return 'May'
        elif re.search('Jun', self.datetime, re.IGNORECASE):
            return 'Jun'
        elif re.search('Jul', self.datetime, re.IGNORECASE):
            return 'Jul'
        elif re.search('Aug', self.datetime, re.IGNORECASE):
            return 'Aug'
        elif re.search('Sep', self.datetime, re.IGNORECASE):
            return 'Sep'
        elif re.search('Nov', self.datetime, re.IGNORECASE):
            return 'Nov'
        elif re.search('Oct', self.datetime, re.IGNORECASE):
            return 'Oct'
        elif re.search('Dec', self.datetime, re.IGNORECASE):
            return 'Dec'
        raise ValueError("Month not present")
