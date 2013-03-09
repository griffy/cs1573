import os
import sys
from experiment import Experiment
from data_initializer import DataInitializer

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Need to pass user folder name\n")
        return

    folder_name = sys.argv[1]
    experiment = Experiment(folder_name)
    experiment.retrieve_data()
    di = DataInitializer(experiment.raw_data_set)
    print experiment.raw_data_set[0][1]         # Just picked a file
    print "======================"
    (names,snames,body) = di.get_mail_elements(experiment.raw_data_set[0][1])
    print "- Primary Names"
    print names
    print "========================"
    print "- Secondary Names"
    print snames
    print "========================"
    print "- Body Text"
    print body
    print "========================"
    
main()
