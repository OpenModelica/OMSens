import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--World3 Sensitivities Calculator--") #un logger especifico para este modulo
# Mine:
import filesystem.files_aux as files_aux
import settings.settings_world3_sweep as world3_settings
import settings.gral_settings as gral_settings
import world3_specific.standard_run_params_defaults

import mos_writer.calculate_sensitivities_mos_writer
import running.run_omc
import analysis.sensitivities_to_parameters_analysis_from_csv


#Aux for GLOBALS:

# System Dynamics .mo to use:
vanilla_SysDyn_mo_path =  world3_settings._sys_dyn_package_vanilla_path.replace("\\","/") # The System Dynamics package without modifications
piecewiseMod_SysDyn_mo_path =  world3_settings._sys_dyn_package_pw_fix_path.replace("\\","/") # Piecewise function modified to accept queries for values outside of range. Interpolate linearly using closest 2 values
populationTankNewVar_SysDyn_mo_path = world3_settings._sys_dyn_package_pop_state_var_new.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run2vermeulenAndJongh_SysDyn_mo_path= world3_settings._sys_dyn_package_v_and_j_run_2.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run3vermeulenAndJongh_SysDyn_mo_path= world3_settings._sys_dyn_package_v_and_j_run_3.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # simpleSensitivitiesCalculator(percentage=5,target_var="Human_Fertility1.Fert_Cont_Facil_PC.Smooth1.Integrator1.y",year_target=2100)
    simpleSensitivitiesCalculator(percentage=5,target_var="population",year_target=2000)
    # simpleSensitivitiesCalculator(percentage=2,target_var="population",year_target=2100)
    # simpleSensitivitiesCalculator(percentage=5,target_var="population",year_target=2100)
    # simpleSensitivitiesCalculator(percentage=10,target_var="population",year_target=2100)

    # allOfDifferentiableVariablesPlusExtraVarsSensitivitiesCalculator(percentage=5,year_target=1901)
    # allOfDifferentiableVariablesPlusExtraVarsSensitivitiesCalculator(percentage=5,year_target=2100)
    return 0

## Predefined sensitivities calculators
def simpleSensitivitiesCalculator(percentage,target_var,year_target):
    logger.info("Calculating simple empirical parameter sensitivities for percentage {perc}, target variable {target_var} and target year {year_target}".format(perc=percentage,target_var=target_var,year_target=year_target))
    output_folder_path = files_aux.makeOutputPath()
    perturbed_csvs_path_and_info_pairs = runModelicaSweepingAllOfW3Params(percentage,year_target,output_folder_path)
    logger.info("Finished running Modelica.")
    # Prepare arguments for "analyze csvs and compare the new value for the variable in the CSV with respect of its value in the standard run"
    analyze_csvs_kwargs = {
        "perturbed_csvs_path_and_info_pairs": perturbed_csvs_path_and_info_pairs,
        "std_run_csv_path": "resource/standard_run.csv",
        "target_vars_list": [target_var],
        "percentage_perturbed":percentage,
        "specific_year":year_target,
        "output_folder_analyses_path": output_folder_path,
        "rms_first_year": 1900 ,# DONT CHANGE! W3-Modelica can't be started on an arbitrary year
        "rms_last_year": year_target,
    }
    logger.info("Analyzing variable sensitivities to parameters from CSVs")
    analysis.sensitivities_to_parameters_analysis_from_csv.analyzeSensitivitiesFromManyVariablesToParametersAndCreateParamVarMatrices(**analyze_csvs_kwargs)
    return 0

def allOfDifferentiableVariablesPlusExtraVarsSensitivitiesCalculator(percentage,year_target):
    logger.info("Calculating empirical parameter sensitivities for percentage {perc}, for all of the differentiable variables in W3 and target year {year_target}".format(perc=percentage,year_target=year_target))
    output_folder_path = files_aux.makeOutputPath()
    perturbed_csvs_path_and_info_pairs = runModelicaSweepingAllOfW3Params(percentage,year_target,output_folder_path)
    logger.info("Finished running Modelica.")
    # Prepare arguments for "analyze csvs and compare the new value for the variable in the CSV with respect of its value in the standard run"
    ## Get the differentiable vars from World3, according to OpenModelica Sensitivity Analysis
    differentiable_vars = list(world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_differentiableVariables_dict.keys()) +list(world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_nonDiffVars_dict.keys()) # transform to list because it's a instance of "dict_keys"
    target_vars_list = differentiable_vars
    analyze_csvs_kwargs = {
        "perturbed_csvs_path_and_info_pairs": perturbed_csvs_path_and_info_pairs,
        "std_run_csv_path": "resource/standard_run.csv",
        "target_vars_list": target_vars_list,
        "percentage_perturbed":percentage,
        "specific_year":year_target,
        "output_folder_analyses_path": output_folder_path,
        "rms_first_year": 1900 ,# DONT CHANGE! W3-Modelica can't be started on an arbitrary year
        "rms_last_year": year_target,
    }
    logger.info("Analyzing variable sensitivities to parameters from CSVs")
    analysis.sensitivities_to_parameters_analysis_from_csv.analyzeSensitivitiesFromManyVariablesToParametersAndCreateParamVarMatrices(**analyze_csvs_kwargs)
    return 0
# Aux funcs
def runModelSweepingParametersInIsolation(percentage, startTime, stopTime, scens_to_run,mo_file,parameters_to_perturbate_tuples,output_folder_path):
    output_mos_path = os.path.join(output_folder_path,gral_settings.mos_script_filename)
    scen_num = scens_to_run[0] # only one scenario for now
    assert len(scens_to_run)==1, "Only one scenario for now"
    model_name = world3_settings._world3_scenario_model_skeleton.format(scen_num=scen_num) #global
    mos_writer.calculate_sensitivities_mos_writer.createMos(mo_file,model_name,parameters_to_perturbate_tuples,output_mos_path,startTime,stopTime, world3_settings.calc_sens_csv_file_name_function)
    logger.info("Running Modelica with specified information")
    running.run_omc.runMosScript(output_mos_path)
    perturbed_csvs_path_and_info_pairs = csvPathAndParameterNameForFolderAndParametersInfo(output_folder_path,parameters_to_perturbate_tuples)
    return perturbed_csvs_path_and_info_pairs

def runModelicaSweepingAllOfW3Params(percentage,year_target,output_folder_path):
    # Reads parameters info from resource/standard_run_params_defaults.py
    params_info_list = world3_specific.standard_run_params_defaults.w3_params_info_list
    # Calculate parameters_to_perturbate_tuples
    parameters_to_perturbate_tuples = calculateParametersPerturbedValueByPercentage(params_info_list,percentage)
    # Prepare arguments for "run model sweeping a list of parameters with a percentage of change, but make each change isolated"
    run_model_kwargs = {
        "percentage": percentage,
        "startTime": 1900 ,# DONT CHANGE! W3-Modelica can't be started on an arbitrary year
        "stopTime": year_target  ,# year to calculate sensitivities from target_vars to parameters
        "scens_to_run" : [1], #The standard run corresponds to the first scenario
        # "mo_file" : vanilla_SysDyn_mo_path, # w3-mod with no modification
        "mo_file" : piecewiseMod_SysDyn_mo_path, # mo that interpolates outwards with values that lie outside of range
        # "mo_file" : populationTankNewVar_SysDyn_mo_path, # mo that has a differentiable population variable added by us and that includes the changes from piecewise function modified
        "parameters_to_perturbate_tuples": parameters_to_perturbate_tuples,
        "output_folder_path":output_folder_path,
    }
    perturbed_csvs_path_and_info_pairs = runModelSweepingParametersInIsolation(**run_model_kwargs)
    return perturbed_csvs_path_and_info_pairs

def calculateParametersPerturbedValueByPercentage(params_info_list,percentage):
    parameters_to_perturbate_tuples = []
    for param_name,param_val,param_desc in params_info_list:
        new_value = param_val+param_val*percentage/100 #for now, we just want the value + a percentage
        parameters_to_perturbate_tuples.append((param_name,param_val,new_value))
    return parameters_to_perturbate_tuples

def csvPathAndParameterNameForFolderAndParametersInfo(output_folder_path,parameters_info):
    perturbed_csvs_path_and_info_pairs = []
    for param_info in parameters_info:
        param_name = param_info[0]
        csv_name = world3_settings.calc_sens_csv_file_name_function(param_name)
        csv_path = os.path.join(output_folder_path,csv_name)
        perturbed_csvs_path_and_info_pairs.append((csv_path,param_info))
    return perturbed_csvs_path_and_info_pairs



# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
