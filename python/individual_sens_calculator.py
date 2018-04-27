# STD
import json
import logging  # instead of prints
import os
import sys

# Ours
import analysis.indiv_sens
import filesystem.files_aux as files_aux
import mos_writer.calculate_sensitivities_mos_writer
import running.run_omc
import settings.settings_world3_sweep as world3_settings
# We import it for now but the objective is that this script replaces that one
import w3_sens_calculator

# Setup logging
logger = logging.getLogger("-Individual Sens Calculator-")


def main():
    # Logging settings
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Args
    json_path = "resource/test_files/individual/test_00.json"
    # Read json
    logger.info("Reading individual sensitivities test file in path {0}.".format(json_path))
    with open(json_path, 'r') as fp:
        full_json = json.load(fp)
    # Mo file from json
    json_mo_path = full_json["model_mo_path"]
    # Check if it's absolute path or relative path and act accordingly
    is_abs_path = os.path.isabs(json_mo_path)
    if is_abs_path:
        # If it's already an absolute path, there's nothing to do
        mo_file_path = json_mo_path
    else:
        # If it's a relative path, make it absolute
        mo_file_path = os.path.abspath(json_mo_path)
    # Default file names
    output_mos_name = "runPerturbingIndividually.mos"
    std_run_filename = "std_run.csv"
    # Get files paths in output folder
    output_folder_path, output_mos_path, std_run_path = filesPathsInOutputFolder(output_mos_name, std_run_filename)
    # Generate list of params and their perturbed values from their defaults and a percentage to perturb
    parameters_to_perturbate_tuples = listOfParametersPerturbationInfo(full_json["param_names"],
                                                                       full_json["param_vals"], full_json["percentage"])
    # Set .mos creator arguments
    mos_creator_kwargs = {
        "model_name": full_json["model_name"],
        "mo_file": mo_file_path,
        "startTime": full_json["start_time"],
        "stopTime": full_json["stop_time"],
        "parameters_to_perturbate_tuples": parameters_to_perturbate_tuples,
        "output_mos_path": output_mos_path,
        "csv_file_name_modelica_function": world3_settings.calc_sens_csv_file_name_function,
        "std_run_filename": std_run_filename,
    }
    # Call .mos creator
    mos_writer.calculate_sensitivities_mos_writer.createMos(**mos_creator_kwargs)
    # Run .mos
    # ADAPTAR INFO PARA QUE DIGA TODA LA INFO A CORRER (modelo, path, etc):
    # logger.info("Calculating empirical parameter sensitivities for percentage {perc}, for all of the differentiable variables in W3 and target year {year_target}".format(perc=full_json["percentage"])
    # ADAPTAR INFO PARA QUE DIGA TODA LA INFO A CORRER (modelo, path, etc)^
    logger.info("Running Modelica with specified information")
    running.run_omc.runMosScript(output_mos_path)
    # Get csvs paths and info pairs
    perturbed_csvs_path_and_info_pairs = w3_sens_calculator.csvPathAndParameterNameForFolderAndParametersInfo(
        output_folder_path, parameters_to_perturbate_tuples)
    # Assume that the .csv with the standard run data will be called like the following
    # Get the path of the recently ran standard run
    # Calculate sensitivities
    analyze_csvs_kwargs = {
        "perturbed_csvs_path_and_info_pairs": perturbed_csvs_path_and_info_pairs,
        "std_run_csv_path": std_run_path,
        "target_vars": full_json["vars_to_analyze"],
        "percentage_perturbed": full_json["percentage"],
        "specific_year": full_json["stop_time"],
        "output_folder_analyses_path": output_folder_path,
        "rms_first_year": full_json["start_time"],
        "rms_last_year": full_json["stop_time"],
    }
    logger.info("Analyzing variable sensitivities to parameters from CSVs")
    analysis.indiv_sens.completeIndividualSensAnalysis(**analyze_csvs_kwargs)


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


def filesPathsInOutputFolder(output_mos_name, std_run_filename):
    # Make tmp dir
    output_folder_path = files_aux.makeOutputPath()
    # .mos script
    output_mos_path = os.path.join(output_folder_path, output_mos_name)
    # Standard run csv
    std_run_path = os.path.join(output_folder_path, std_run_filename)
    return output_folder_path, output_mos_path, std_run_path


# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
