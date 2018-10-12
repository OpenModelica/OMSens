# STD
import argparse
import json
import os
import sys
import logging

# Ours
import analysis.indiv_sens
import filesystem.files_aux as files_aux
import mos_writer.calculate_sensitivities_mos_writer as sens_mos_writer
import modelica_interface.run_omc as run_omc
import settings.gral_settings

logger = logging.getLogger("-Individual Sens Calculator-")
script_description = "Calculate variables sensitivities to parameters when perturbed in isolation"


def main():
    # Logging settings
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Get arguments from command line call
    json_file_path, dest_folder_path_arg = getCommandLineArguments()
    # Args
    dest_folder_path = finalDestFolderPath( dest_folder_path_arg)
    perturbateAndAnalyzeFromJsonToPath(json_file_path, dest_folder_path)
    return 0


def perturbateAndAnalyzeFromJsonToPath(json_file_path, dest_folder_path):
    # Read JSON
    with open(json_file_path, 'r') as fp:
        full_json = json.load(fp)
    model_file_path = files_aux.moFilePathFromJSONMoPath(full_json["model_mo_path"])
    perturbateAndAnalyze_kwargs = {
        "model_name"            : full_json["model_name"],
        "model_file_path"       : model_file_path,
        "start_time"            : full_json["start_time"],
        "stop_time"             : full_json["stop_time"],
        "parameters_to_perturb" : full_json["parameters_to_perturb"],
        "percentage"            : full_json["percentage"],
        "target_vars"           : full_json["vars_to_analyze"],
        "dest_folder_path"      : dest_folder_path,
    }
    perturbateAndAnalyze(**perturbateAndAnalyze_kwargs)


def perturbateAndAnalyze( model_name, model_file_path, start_time, stop_time, parameters_to_perturb, percentage,
                              target_vars, dest_folder_path ):
    # Create simulations folder
    perturbations_folder_name = "simulation"
    perturbations_folder_path = os.path.join(dest_folder_path, perturbations_folder_name)
    files_aux.makeFolderWithPath(perturbations_folder_path)
    # Create analysis folder
    analysis_folder_name = "analysis"
    analysis_folder_path = os.path.join(dest_folder_path, analysis_folder_name)
    files_aux.makeFolderWithPath(analysis_folder_path)
    # Prepare kwargs for perturbator
    perturbator_kwargs = {
        "model_name": model_name,
        "model_file_path": model_file_path,
        "start_time": start_time,
        "stop_time": stop_time,
        "parameters": parameters_to_perturb,
        "perc_perturb": percentage,
        "build_folder_path": perturbations_folder_path,
    }
    # Initialize perturbator
    perturbator = analysis.indiv_sens.ParametersIsolatedPerturbator(**perturbator_kwargs)
    # Run simulations using perturbator
    logger.info("Running Modelica with specified information")
    isolated_perturbations_results = perturbator.runSimulations(perturbations_folder_path)
    analyze_csvs_kwargs = {
        "isolated_perturbations_results": isolated_perturbations_results,
        "target_vars": target_vars,
        "percentage_perturbed": percentage,
        "specific_year": stop_time,
        "output_folder_analyses_path": analysis_folder_path,
        "rms_first_year": start_time,
        "rms_last_year": stop_time,
    }
    logger.info("Analyzing variable sensitivities to parameters from CSVs")
    # Calculate sensitivities
    analysis_results = analysis.indiv_sens.completeIndividualSensAnalysis(**analyze_csvs_kwargs)
    # Get the dict with the paths
    paths_dict = analysis_results["paths"]
    # Write paths dict as json
    paths_json_str = json.dumps(paths_dict, sort_keys=True, indent=2)
    paths_json_file_name = "result.json"
    paths_json_file_path = os.path.join(dest_folder_path, paths_json_file_name)
    files_aux.writeStrToFile(paths_json_str, paths_json_file_path)
    logger.info("Finished. The file {0} has all the analysis files paths.".format(paths_json_file_path))


def listOfParametersPerturbationInfo(param_names, param_vals, percentage):
    parameters_to_perturbate_tuples = []
    # Iterate parameters name and default info
    for p_name, p_val in zip(param_names, param_vals):
        # Calculate parameter value from percentage to perturb
        perturbed_val = p_val * (1 + percentage / 100)
        # Create tuple and add it to list of tuples
        param_tuple = (p_name, p_val, perturbed_val)
        parameters_to_perturbate_tuples.append(param_tuple)
    return parameters_to_perturbate_tuples


def finalDestFolderPath(dest_folder_path_arg):
    # Make dest folder path in this projects root if none indicated in command line
    if not dest_folder_path_arg:
        dest_folder_path = files_aux.makeOutputPath("indiv_sens_analysis")
    else:
        dest_folder_path = dest_folder_path_arg
    # .mos script
    return dest_folder_path


def csvPathAndParameterNameForFolderAndParametersInfo(dest_folder_path, parameters_info):
    perturbed_csvs_path_and_info_pairs = []
    for param_info in parameters_info:
        param_name = param_info[0]
        csv_name = settings.gral_settings.calc_sens_csv_file_name_function(param_name)
        csv_path = os.path.join(dest_folder_path, csv_name)
        perturbed_csvs_path_and_info_pairs.append((csv_path, param_info))
    return perturbed_csvs_path_and_info_pairs

def getCommandLineArguments():
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('test_file_path', metavar='test_file_path',
                        help='The path to the file with the experiment specifications.')
    parser.add_argument('--dest_folder_path', metavar='dest_folder_path',
                        help='Optional: The destination folder where to write the analysis files')
    args = parser.parse_args()
    return args.test_file_path, args.dest_folder_path


# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()

