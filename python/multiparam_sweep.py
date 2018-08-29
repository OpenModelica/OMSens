# Std
import sys
import argparse
import logging  # instead of prints

logger = logging.getLogger("-Individual Sens Calculator-")
script_description = "Run a multiparemeter sweep and plot the results"


# Mine
def main():
    # Logging settings
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Get arguments from command line call
    json_file_path, dest_folder_path_arg = getCommandLineArguments()


def getCommandLineArguments():
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('test_file_path', metavar='test_file_path',
                        help='The file path to the test file containing the CSVs to plot, the variables, the title, etc.')
    parser.add_argument('--dest_folder_path', metavar='dest_folder_path',
                        help='Optional: The destination folder where to write the analysis files')
    args = parser.parse_args()
    return args.test_file_path, args.dest_folder_path

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
