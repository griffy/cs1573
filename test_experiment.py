import os
import sys
from experiment import Experiment

def main():
        if len(sys.argv) < 2:
                sys.stderr.write("Need to pass user folder name\n")
                return

        folder_name = sys.argv[1]
        experiment = Experiment(folder_name)
	experiment.retrieve_data()
	di = DataInitializer(experiment.raw_data_set)
	(names, secondary_names, body_text) = di.get_mail_elements("/Users/rishisadhir/Dropbox/School/cs1573/term-project/main/cs1573/data/beck-s/moscoso__mike/4.")
	print names
	print secondary_names
	print body_text
	
main()
