import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--World3 Sensitivities Calculator--") #un logger especifico para este modulo
# Mine:
import mos_writer.mos_script_factory as mos_script_factory
import sweeping.run_and_plot_model as run_and_plot_model
import filesystem.files_aux as files_aux
import settings.settings_world3_sweep as world3_settings
import settings.gral_settings as gral_settings
import resource.standard_run_params_defaults

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
    simpleSensitivitiesCalculator(percentage=2,var_target="population",year_target=2100)
    simpleSensitivitiesCalculator(percentage=5,var_target="population",year_target=2100)
    simpleSensitivitiesCalculator(percentage=10,var_target="population",year_target=2100)

## Predefined sensitivities calculators
def simpleSensitivitiesCalculator(percentage,var_target,year_target):
    # Reads parameters info from resource/standard_run_params_defaults.py
    # Calculate parameters_to_perturbate_tuples
    parameters_to_perturbate_tuples = []
    params_info_list = resource.standard_run_params_defaults.w3_params_info_list
    for param_name,param_val in params_info_list:
        new_value = param_val+param_val*percentage/100 #for now, we just want the value + a percentage
        parameters_to_perturbate_tuples.append((param_name,param_val,new_value))
    kwargs = {
        "target_vars":["population"],
        "percentage": percentage,
        "startTime": 1900 ,# DONT CHANGE! W3-Modelica can't be started on an arbitrary year
        "stopTime": year_target  ,# year to calculate sensitivities from target_vars to parameters
        "scens_to_run" : [1], #The standard run corresponds to the first scenario
        "mo_file" : piecewiseMod_SysDyn_mo_path, # mo that interpolates outwards with values that lie outside of range
        "plot_std_run": True, #Choose to plot std run alognside this test results
        "parameters_to_perturbate_tuples": parameters_to_perturbate_tuples,
    }
    setUpSensitivitiesCalculationAndRun(**kwargs)
def setUpSensitivitiesCalculationAndRun(target_vars,percentage, startTime, stopTime, scens_to_run , mo_file , plot_std_run, parameters_to_perturbate_tuples):
    output_folder_path = files_aux.makeOutputPath()
    output_mos_path = os.path.join(output_folder_path,gral_settings.mos_script_filename)
    scen_num = scens_to_run[0] # only one scenario for now
    assert len(scens_to_run)==1, "Only one scenario for now"
    model_name = world3_settings._world3_scenario_model_skeleton.format(scen_num=scen_num) #global
    mos_writer.calculate_sensitivities_mos_writer.createMos(mo_file,model_name,parameters_to_perturbate_tuples,output_mos_path,startTime,stopTime, world3_settings.calc_sens_csv_file_name_function)
    running.run_omc.runMosScript(output_mos_path)
    perturbed_csvs_path_and_info_pairs = csvPathAndParameterNameForFolderAndParametersInfo(output_folder_path,parameters_to_perturbate_tuples)

    kwargs = {
        "perturbed_csvs_path_and_info_pairs": perturbed_csvs_path_and_info_pairs,
        "std_run_csv_path": "resource/standard_run.csv",
        "target_var": "population",
        "percentage_perturbed":percentage,
        "year":stopTime,
        "output_analysis_path": os.path.join(output_folder_path,"sens_analysis.csv"),
        "rms_first_year": startTime,
        "rms_last_year": stopTime,
    }
    analysis.sensitivities_to_parameters_analysis_from_csv.analyzeSensitivitiesFromVariableToParametersFromCSVs(**kwargs)
# def analyzeSensitivitiesFromVariableToParametersFromCSVs(perturbed_csvs_path_and_info_pairs,target_var,percentage_perturbed,year,std_run_csv_path,output_analysis_path):
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
