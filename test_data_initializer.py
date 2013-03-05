import os
import sys
from data_initializer import DataInitializer

def main():
	if len(sys.argv) < 2:
		sys.stderr.write("Need to pass user folder name\n")
		return 

	folder_name = sys.argv[1]
	data_initializer = DataInitializer(folder_name)
	data_initializer.initialize_mapping()

	data_initializer.print_class_document_map()

main()