import os
import sys
from experiment import Experiment
from data_initializer import DataInitializer

def main():
    try:
        folder_name = sys.argv[1]
        experiment = Experiment(folder_name)
    except IndexError:
        experiment = Experiment()
    experiment.retrieve_data()
    di = DataInitializer(experiment.raw_data_set)
    di.print_data_set()
        
main()
