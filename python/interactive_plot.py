# Imports:
# Base:
import sys
import argparse
import os
from datetime import datetime
import inspect
import logging  # en reemplazo de los prints

logger = logging.getLogger("--Interactive plot--")  # un logger especifico para este modulo
# My imports
# Globals:
script_description = """Interactive plot. Pass CSVs paths as command line arguments and then continue to pass arguments interactively (such as title, subtitle, etc). The paths are passed as command line because they are easier to get than by typing."""
dest_folder_name = "interactive_plots"
import filesystem.files_aux
import plotting.plot_csv


def main():
    logging.basicConfig(level=logging.DEBUG)  # to show on stdout and only info
    csvs_paths_list = getCommandLineArguments()
    csvs_paths_list_str = "\n".join(["    *:" + x for x in csvs_paths_list])
    print("Received the following CSV files to plot:\n %s\n CTRL-C if not OK." % csvs_paths_list_str)
    one_var_plot_bool = askIfOneOrTwoVarsPlot()
    if one_var_plot_bool:
        # Only one var in the plot:
        plotter_kwargs = getInteractiveArgumentsForOneVarPlot(csvs_paths_list)
        plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)
    else:
        # Plot 2 vars in the same plot with the left y axis corresponding to the first var and the right one to the second var
        plotter_kwargs = getInteractiveArgumentsForTwoVarsPlot(csvs_paths_list)
        plotting.plot_csv.twoVarsMultipleCSVsPlot(**plotter_kwargs)
    logger.debug("Plotted succesfully")


def askIfOneOrTwoVarsPlot():
    one_or_two = query_1_or_2("1 Only one variable plot.     2 for 2 variables together in same plot.\n")
    one_var_plot_bool = 1 == one_or_two
    return one_var_plot_bool


def getInteractiveArgumentsForTwoVarsPlot(csvs_paths_list):
    plot_var_left = input("Left y axis var?\n  ")
    plot_var_right = input("Right y axis var?\n  ")
    plot_title = input("Plot title?\n  ")
    plot_subtitle = input("Plot subtitle?\n  ")
    plot_footer = input("Plot footer?\n  ").replace("\\n", "\n")  # input function cant handle \n. The replace fixes it

    csvs_path_label_pair_list = []
    for csv_path in csvs_paths_list:
        csv_label = input("Label for file: %s?\n  " % csv_path)
        csvs_path_label_pair_list.append((csv_path, csv_label))

    print("Now x label. That is, the left limit and the right limits of the plot\n")
    left_limit = query_int("  Left limit? (xrange first position)\n   ")
    right_limit = query_int("  Right limit? (xrange right position)\n   ")
    x_range = [left_limit, right_limit]
    include_stdrun = query_yes_no("Include World3 standard variable run in the plot?")
    output_folder_path = filesystem.files_aux.makeOutputPath(dest_folder_name)
    print("Plotting to:\n %s" % output_folder_path)
    #    # For now, the plot_file_name is fixed as the plot_var
    #    # plot_file_name = input("Plot name without extension? \n    (Example: 'population', 'population_6_parameters_perturbed',etc)\n  ")
    plotter_kwargs = {
        "plot_title": plot_title,
        "subtitle": plot_subtitle,
        "footer": plot_footer,
        "csvs_path_label_pair_list": csvs_path_label_pair_list,
        "x_range": x_range,
        "output_folder_path": output_folder_path,
        "extra_ticks": [],  # no extra ticks input available for now (needs a variable amount of inputs)
        "include_stdrun": include_stdrun,
        "vars_list_pairs": [(plot_var_left, plot_var_right)],
    }
    return plotter_kwargs


def getInteractiveArgumentsForOneVarPlot(csvs_paths_list):
    plot_var = input("Variable to plot?\n  ")
    plot_title = input("Plot title?\n  ")
    plot_subtitle = input("Plot subtitle?\n  ")
    plot_footer = input("Plot footer?\n  ").replace("\\n", "\n")  # input function cant handle \n. The replace fixes it

    csvs_path_label_pair_list = []
    for csv_path in csvs_paths_list:
        csv_label = input("Label for file: %s?\n  " % csv_path)
        csvs_path_label_pair_list.append((csv_path, csv_label))

    print("Now x label. That is, the left limit and the right limits of the plot\n")
    left_limit = query_int("  Left limit? (xrange first position)\n   ")
    right_limit = query_int("  Right limit? (xrange right position)\n   ")
    x_range = [left_limit, right_limit]
    include_stdrun = query_yes_no("Include World3 standard variable run in the plot?")
    output_folder_path = filesystem.files_aux.makeOutputPath(dest_folder_name)
    print("Plotting to:\n %s" % output_folder_path)
    #    # For now, the plot_file_name is fixed as the plot_var
    #    # plot_file_name = input("Plot name without extension? \n    (Example: 'population', 'population_6_parameters_perturbed',etc)\n  ")
    plotter_kwargs = {
        "plot_title": plot_title,
        "subtitle": plot_subtitle,
        "footer": plot_footer,
        "csvs_path_label_pair_list": csvs_path_label_pair_list,
        "x_range": x_range,
        "output_folder_path": output_folder_path,
        "extra_ticks": [],  # no extra ticks input available for now (needs a variable amount of inputs)
        "include_stdrun": include_stdrun,
        "vars_list": [plot_var],  # only one var plottable for now (needs a variable amount of inputs)
    }
    return plotter_kwargs


def query_int(question):
    while True:
        choice = input(question)
        try:
            integer_input = int(choice)
            return integer_input
        except ValueError:
            print("Please respond with a valid integer\n")


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' "
                  "(or 'y' or 'n').\n")


def getCommandLineArguments():
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('csvs_paths_list', metavar='csvs_paths_list', nargs="+",
                        help='The csvs paths (preferably absolute paths) to plot in the same plot.')
    args = parser.parse_args()
    csvs_paths_list = args.csvs_paths_list
    return csvs_paths_list


def makeDirFromCurrentTimestamp(dest_path):
    logger.debug("Making timestamp dir")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    dateAndTime = datetime.now()
    new_folder_path = os.path.join(dest_path, dateAndTime.strftime('%Y-%m-%d/%H_%M_%S'))
    os.makedirs(new_folder_path)
    return new_folder_path


def destPath():
    tmp_path = tmpPath()
    return os.path.join(tmp_path, "csv_analysis")


def tmpPath():
    currentdir = currentDir()
    parentdir = parentDir(currentdir)
    return os.path.join(parentdir, "tmp")


def query_1_or_2(query_question):
    while True:
        choice = input(query_question)
        try:
            integer_input = int(choice)
            if integer_input in [1, 2]:
                return integer_input
            else:
                print("Please respond with 1 or 2.\n")
        except ValueError:
            print("Please respond with 1 or 2.\n")


if __name__ == "__main__":
    main()
