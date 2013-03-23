import sys
from dataset import DataInitializer

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Need to pass user folder name\n")
        return

    user_folder_uri = sys.argv[1]
    data_initializer = DataInitializer(user_folder_uri)
    example_type, examples = data_initializer.preprocess()

    with open(user_folder_uri + "_examples.txt", 'w') as example_file:
        # write the schema
        example_file.write(example_type.features[0])
        for feature in example_type.features[1:]:
            example_file.write(',' + feature)
        example_file.write('\n')

        # write each example
        for example in examples:
            example_file.write(str(example) + '\n')

main()