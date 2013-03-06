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
        experiment.print_raw_data_set()

main()
