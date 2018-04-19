# STD
import os
import sys
import inspect
import json
import logging # instead of prints
logger = logging.getLogger("-Individual Sens Calculator-")
# Ours
import analysis.sensitivities_to_parameters_analysis_from_csv
import mos_writer.calculate_sensitivities_mos_writer
import settings.settings_world3_sweep as world3_settings
import running.run_omc
import filesystem.files_aux as files_aux
# We import it for now but the objective is that this script replaces that one
import w3_sens_calculator

def main():
    # Logging settings
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Args
    json_path = "resource/test_files/individual/test_00.json"
    # Read json
    logger.info("Reading individual sensitivities test file in path {0}.".format(json_path))
    with open(json_path, 'r') as fp:
        full_json =  json.load(fp)
    # Make tmp dir
    output_folder_path = files_aux.makeOutputPath()
    # Set relative paths as absolute paths using this scripts path as base
    #  Folders
    current_dir   = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    resource_path = os.path.join(current_dir,"resource")
    #  Files
    #   Modelica model file
    mo_file          = os.path.join(resource_path,full_json["model_mo_path"])
    #   .mos script
    output_mos_name  = "runPerturbingIndividually.mos"
    output_mos_path  = os.path.join(output_folder_path,output_mos_name)
    #   Standard run csv
    std_run_filename = "std_run.csv"
    std_run_path     = os.path.join(output_folder_path,std_run_filename)
    # Generate list of params and their perturbed values from their defaults and a percentage to perturb
    parameters_to_perturbate_tuples = [(p_name,p_val,p_val*(1+full_json["percentage"]/100)) for p_name,p_val in zip(full_json["param_names"], full_json["param_vals"])]
    # Set .mos creator arguments
    mos_creator_kwargs = {
        "model_name"                      : full_json["model_name"],
        "mo_file"                         : mo_file,
        "startTime"                       : full_json["start_time"],
        "stopTime"                        : full_json["stop_time"],
        "parameters_to_perturbate_tuples" : parameters_to_perturbate_tuples,
        "output_mos_path"                 : output_mos_path,
        "csv_file_name_modelica_function" : world3_settings.calc_sens_csv_file_name_function,
        "std_run_filename"                : std_run_filename,
    }
    # Call .mos creator
    mos_writer.calculate_sensitivities_mos_writer.createMos(**mos_creator_kwargs)
    # Run .mos
# ADAPTAR INFO PARA QUE DIGA TODA LA INFO A CORRER (modelo, path, etc):
    # logger.info("Calculating empirical parameter sensitivities for percentage {perc}, for all of the differentiable variables in W3 and target year {year_target}".format(perc=full_json["percentage"])
# ADAPTAR INFO PARA QUE DIGA TODA LA INFO A CORRER (modelo, path, etc)^
    logger.info("Running Modelica with specified information")
# DESCOMENTAR:
    running.run_omc.runMosScript(output_mos_path)
    # Get csvs paths and info pairs
    perturbed_csvs_path_and_info_pairs = w3_sens_calculator.csvPathAndParameterNameForFolderAndParametersInfo(output_folder_path,parameters_to_perturbate_tuples)
    # Assume that the .csv with the standard run data will be called like the following
    # Get the path of the recently ran standard run
    # Calculate sensitivities
    analyze_csvs_kwargs = {
        "perturbed_csvs_path_and_info_pairs" : perturbed_csvs_path_and_info_pairs,
        "std_run_csv_path"                   : std_run_path,
        "target_vars"                   : full_json["vars_to_analyze"],
        "percentage_perturbed"               : full_json["percentage"],
        "specific_year"                      : full_json["stop_time"],
        "output_folder_analyses_path"        : output_folder_path,
        "rms_first_year"                     : full_json["start_time"],
        "rms_last_year"                      : full_json["stop_time"],
    }
    logger.info("Analyzing variable sensitivities to parameters from CSVs")
    analysis.sensitivities_to_parameters_analysis_from_csv.analyzeSensitivitiesFromManyVariablesToParametersAndCreateParamVarMatrices(**analyze_csvs_kwargs)
# DESCOMENTAR^

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()

