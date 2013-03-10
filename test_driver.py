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
    di = DataInitializer()
    di.initialize_matrix(experiment.raw_data_set)
    di.print_global_names()

main()
