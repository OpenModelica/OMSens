# Std
import os
import sys
import argparse
import logging  # instead of prints
import json
import filesystem.files_aux as files_aux
import pandas

# Project
import vectorial.model_optimizer as model_optimizer_f
import modelica_interface.build_model as build_model
import plotting.plot_vectorial as plot_vect_f

logger = logging.getLogger("-Vectorial Sens Calculator-")
script_description = "Find parameters values that maximize or minimize a variable"


# Mine
def main():
    # Logging settings
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Get arguments from command line call
    json_file_path, dest_folder_path_arg = getCommandLineArguments()
    # Define where to write the results
    if not dest_folder_path_arg:
        dest_folder_path = files_aux.makeOutputPath("vectorial_analysis")
    else:
        dest_folder_path = dest_folder_path_arg

    # Read JSON again (both reads should be refactored into one)
    analyzeFromJSON(dest_folder_path, json_file_path)


def analyzeFromJSON(dest_folder_path, json_file_path):
    with open(json_file_path, 'r') as fp:
        full_json = json.load(fp)
    # Prepare init args
    model_mo_path = files_aux.moFilePathFromJSONMoPath(full_json["model_mo_path"])
    optim_kwargs = \
        {
            "model_file_path"      : model_mo_path,
            "target_var_name"      : full_json["target_var_name"],
            "build_folder_path"    : dest_folder_path,
            "parameters_to_perturb": full_json["parameters_to_perturb"],
            "model_name"           : full_json["model_name"],
            "start_time"           : full_json["start_time"],
            "stop_time"            : full_json["stop_time"],
            "max_or_min"           : full_json["max_or_min"],

        }
    # Initialize optimizer
    model_optimizer = model_optimizer_f.ModelOptimizer(**optim_kwargs)
    # Run optimization
    optim_result = model_optimizer.optimize(full_json["percentage"], full_json["epsilon"])
    # We compile the model again for now to avoid having remnants of the optimization in its compiled model
    # Initialize builder
    model_builder = build_model.ModelicaModelBuilder(full_json["model_name"], full_json["start_time"],
                                                     full_json["stop_time"], model_mo_path)
    # Make sub-folder for plots
    plots_folder_name = "plots"
    plots_folder_path = os.path.join(dest_folder_path,plots_folder_name)
    files_aux.makeFolderWithPath(plots_folder_path)
    # Make sub-folder for new model
    model_folder_name = "aux_folder" # in Windows we can't use "aux" for folder names
    model_folder_path = os.path.join(plots_folder_path,model_folder_name)
    files_aux.makeFolderWithPath(model_folder_path)
    # Build model
    compiled_model = model_builder.buildToFolderPath(model_folder_path)
    # Simulate model for x0
    x0_csv_name = "x0_run.csv"
    x0_csv_path = os.path.join(model_folder_path,x0_csv_name)
    x0_simu_result = compiled_model.simulate(x0_csv_path, params_vals_dict=optim_result.x0)
    # Simulate model for x_opt
    x_opt_csv_name = "x_opt_run.csv"
    x_opt_csv_path = os.path.join(model_folder_path,x_opt_csv_name)
    x_opt_simu_result = compiled_model.simulate(x_opt_csv_path, params_vals_dict=optim_result.x_opt)
    # Read df from CSVs
    df_x0_run = pandas.read_csv(x0_csv_path)
    df_x_opt_run = pandas.read_csv(x_opt_csv_path)
    # Initialize plotter
    vect_plotter = plot_vect_f.VectorialPlotter(optim_result, df_x0_run, df_x_opt_run)
    # Plot in folder
    plot_path = vect_plotter.plotInFolder(plots_folder_path)


    # Prepare JSON output dict
    vect_json_dict = {
        "x0"       : optim_result.x0,
        "x_opt"    : optim_result.x_opt,
        "f(x0)"    : optim_result.f_x0,
        "f(x)_opt" : optim_result.f_x_opt,
        "stop_time": optim_result.stop_time,
        "variable" : optim_result.variable_name,
        "plot_path": plot_path,
    }
    # Write dict as json
    optim_json_str = json.dumps(vect_json_dict, sort_keys=True, indent=2)
    optim_json_file_name = "result.json"
    optim_json_file_path = os.path.join(dest_folder_path, optim_json_file_name)
    files_aux.writeStrToFile(optim_json_str, optim_json_file_path)
    logger.info("Finished. The file {0} has the optimization results.".format(optim_json_file_path))


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

