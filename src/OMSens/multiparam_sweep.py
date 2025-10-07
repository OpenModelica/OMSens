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

logger = logging.getLogger("-Multiparameter Sweep-")
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
    sweepAndPlotFromJSON(dest_folder_path, json_file_path)


def sweepAndPlotFromJSON(dest_folder_path, json_file_path):
    with open(json_file_path, 'r') as fp:
        full_json = json.load(fp)
    # Prepare sweep init args
    model_mo_path = files_aux.moFilePathFromJSONMoPath(full_json["model_mo_path"])
    sweep_kwargs = \
        {
            "model_name"                  : full_json["model_name"],
            "model_file_path"             : model_mo_path,
            "start_time"                  : full_json["start_time"],
            "stop_time"                   : full_json["stop_time"],
            "perturbation_info_per_param" : full_json["parameters_to_sweep"],
            "fixed_params"                : full_json["fixed_params"],
            "build_folder_path"           : dest_folder_path,

        }
    # Initialize sweeper
    sweep_runner = running.sweep.ParametersSweeper(**sweep_kwargs)
    # Run sweep
    sweep_results = sweep_runner.runSweep(dest_folder_path)
    # Initialize sweep results plotter
    sweep_plotter = plot_sweep.SweepPlotter(sweep_results)
    # Make folder for plots
    plot_folder_path = os.path.join(dest_folder_path, "plots")
    files_aux.makeFolderWithPath(plot_folder_path)
    # Plot sweep for each var
    vars_plots_paths = {}
    for var_name in full_json["vars_to_analyze"]:
        plot_path = sweep_plotter.plotInFolder(var_name, plot_folder_path)
        vars_plots_paths[var_name] = plot_path
    # Add sweep plots to paths dict
    paths_dict = \
        {
            "sweep_plots": vars_plots_paths,
        }
    # Write paths dict as json
    paths_json_str = json.dumps(paths_dict, sort_keys=True, indent=2)
    paths_json_file_name = "result.json"
    paths_json_file_path = os.path.join(dest_folder_path, paths_json_file_name)
    files_aux.writeStrToFile(paths_json_str, paths_json_file_path)
    logger.info("Finished. The file {0} has all the sweep files paths.".format(paths_json_file_path))


# Auxs
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
