# Std
import os
import sys
import argparse
import logging  # instead of prints
import json
import filesystem.files_aux as files_aux

# Mine
import running.sweep
import plotting.plot_sweep as plot_sweep

logger = logging.getLogger("-Individual Sens Calculator-")
script_description = "Run a multiparemeter sweep and plot the results"


# Mine
def main():
    # Logging settings
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Get arguments from command line call
    json_file_path, dest_folder_path_arg = getCommandLineArguments()
    # Define where to write the results
    if not dest_folder_path_arg:
        dest_folder_path = files_aux.makeOutputPath("multiparameter_sweep")
    else:
        dest_folder_path = dest_folder_path_arg

    # Read JSON again (both reads should be refactored into one)
    with open(json_file_path, 'r') as fp:
        full_json = json.load(fp)
    # Prepare sweep init args
    model_mo_path = moFilePathFromJSONMoPath(full_json["model_mo_path"])
    sweep_kwargs = \
        {
            "model_name": full_json["model_name"],
            "model_file_path": model_mo_path,
            "start_time": full_json["start_time"],
            "stop_time": full_json["stop_time"],
            "perturbation_info_per_param": full_json["parameters_to_sweep"],
            "build_folder_path": dest_folder_path,

        }
    # Initialize sweeper
    sweep_runner = running.sweep.ParametersSweeper(**sweep_kwargs)
    # Run sweep
    sweep_results = sweep_runner.runSweep(dest_folder_path)
    # Initialize sweep results plotter
    sweep_plotter = plot_sweep.SweepPlot(sweep_results)
    # Plot sweep for each var
    plot_folder_path = os.path.join(dest_folder_path, "plots")
    files_aux.makeFolderWithPath(plot_folder_path)
    for var_name in full_json["vars_to_analyze"]:
        sweep_plotter.plotInFolder(var_name, plot_folder_path)


# Auxs
def moFilePathFromJSONMoPath(json_mo_path):
    # Check if it's absolute path or relative path and act accordingly
    is_abs_path = os.path.isabs(json_mo_path)
    if is_abs_path:
        # If it's already an absolute path, there's nothing to do
        mo_file_path = json_mo_path
    else:
        # If it's a relative path, make it absolute
        mo_file_path = os.path.abspath(json_mo_path)
    return mo_file_path

def getCommandLineArguments():
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('test_file_path', metavar='test_file_path',
                        help='The path to the file with the experiment specifications.')
    parser.add_argument('--dest_folder_path', metavar='dest_folder_path',
                        help='Optional: The destination folder where to write the sweep files')
    args = parser.parse_args()
    return args.test_file_path, args.dest_folder_path

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
