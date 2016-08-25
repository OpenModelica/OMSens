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

#Aux for GLOBALS:

# System Dynamics .mo to use:
vanilla_SysDyn_mo_path =  world3_settings._sys_dyn_package_vanilla_path.replace("\\","/") # The System Dynamics package without modifications
piecewiseMod_SysDyn_mo_path =  world3_settings._sys_dyn_package_pw_fix_path.replace("\\","/") # Piecewise function modified to accept queries for values outside of range. Interpolate linearly using closest 2 values
populationTankNewVar_SysDyn_mo_path = world3_settings._sys_dyn_package_pop_state_var_new.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run2vermeulenAndJongh_SysDyn_mo_path= world3_settings._sys_dyn_package_v_and_j_run_2.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run3vermeulenAndJongh_SysDyn_mo_path= world3_settings._sys_dyn_package_v_and_j_run_3.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    simpleSensitivitiesCalculator(percentage=10,var_target="population",year_target=1950)

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
    "startTime": 1900 ,# DONT CHANGE! W3-Modelica can't be started on an arbitrary year
    "stopTime": 1950  ,# year to calculate sensitivities from target_vars to parameters
    "scens_to_run" : [1], #The standard run corresponds to the first scenario
    "mo_file" : piecewiseMod_SysDyn_mo_path, # mo that interpolates outwards with values that lie outside of range
    "plot_std_run": True, #Choose to plot std run alognside this test results
    "parameters_to_perturbate_tuples": parameters_to_perturbate_tuples,
    }
    setUpSensitivitiesCalculationAndRun(**kwargs)
def setUpSensitivitiesCalculationAndRun(target_vars, startTime, stopTime, scens_to_run , mo_file , plot_std_run, parameters_to_perturbate_tuples):
    output_folder_path = files_aux.makeOutputPath()
    output_mos_path = os.path.join(output_folder_path,gral_settings.mos_script_filename)
    scen_num = scens_to_run[0] # only one scenario for now
    assert len(scens_to_run)==1, "Only one scenario for now"
    model_name = world3_settings._world3_scenario_model_skeleton.format(scen_num=scen_num) #global
    mos_writer.calculate_sensitivities_mos_writer.createMos(mo_file,model_name,parameters_to_perturbate_tuples,output_mos_path,startTime,stopTime, world3_settings.calc_sens_csv_file_name_skeleton)
    running.run_omc.runMosScript(output_mos_path)
# def createMos(mo_file,model_name,parameters_to_perturbate_tuples,output_mos_path,startTime,stopTime,csv_file_name_modelica):
# BORRAR DESDE ACA: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    # iterations = 9;
    # kwargs = {
    # "plot_vars":["Industrial_Investment1Industrial_Outputcapital_util_fr"],
    # # "plot_vars":["Industrial_Investment1Industrial_Outputcapital_util_fr", "industrial_output", "serv_out_pc", "ind_out_pc", "s_fioa_serv",],
    # "startTime": 1900 ,# year to start the simulation (1900 example)
    # "stopTime": 2000  ,# year to end the simulation (2100 for example)
    # "scens_to_run" : [1], #The standard run corresponds to the first scenario
    # "iterations" : iterations,
    # "sweep_vars":  ["p_ind_cap_out_ratio_1"], # Examples: SPECIAL_policy_years, ["nr_resources_init"]
    # "sweep_value_formula_str" : deltaBeforeAndAfter(p=3,delta=1/12,iterations=iterations), # Sweep floor(iterations/2) times before and after p changing by a percentage of delta*100
    # "fixed_params" : [],  # No fixed parameter changes. Example: [("nr_resources_init",6.3e9),("des_compl_fam_size_norm",2),...]
    # # "mo_file" : vanilla_SysDyn_mo_path, # Mo without modifications
    # "mo_file" : piecewiseMod_SysDyn_mo_path, # mo that interpolates outwards with values that lie outside of range
    # "plot_std_run": False, #Choose to plot std run alognside this test results
    # }
    # setUpSweepsAndRun(**kwargs)
# BORRAR HASTA ACA: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

#World3 specific:
# def setUpSweepsAndRun(iterations,sweep_vars,sweep_value_formula_str,fixed_params,plot_vars,startTime,stopTime,scens_to_run,mo_file,plot_std_run=False):
#     #The "root" output folder path.
#     output_path = files_aux.makeOutputPath()
#     #Create scenarios from factory
#     scenarios = []
#     for i in scens_to_run:
#         initial_factory_for_scen_i = initialFactoryForWorld3Scenario(scen_num=i,start_time=startTime,stop_time=stopTime,mo_file=mo_file,fixed_params=fixed_params,sweep_vars=sweep_vars)
#         scenario_tuple =("scenario_"+str(i),initial_factory_for_scen_i)
#         scenarios.append(scenario_tuple)
#     doScenariosSet(scenarios, plot_vars=plot_vars,iterations=iterations,output_root_path=output_path, sweep_value_formula_str=sweep_value_formula_str,plot_std_run=plot_std_run)
# def doScenariosSet(scenarios,plot_vars,iterations,output_root_path,sweep_value_formula_str,plot_std_run):
#     for folder_name,initial_scen_factory in scenarios:
#         logger.debug("Running scenario {folder_name}".format(folder_name=folder_name))
#         os.makedirs(os.path.join(output_root_path,folder_name))
#         run_and_plot_model.createSweepRunAndPlotForModelInfo(initial_scen_factory,plot_vars=plot_vars,iterations=iterations,output_folder_path=os.path.join(output_root_path,folder_name),sweep_value_formula_str=sweep_value_formula_str,csv_file_name_modelica_skeleton=world3_settings.csv_file_name_modelica_skeleton,csv_file_name_python_skeleton=world3_settings.csv_file_name_python_skeleton,plot_std_run=plot_std_run)
# def initialFactoryForWorld3Scenario(scen_num,start_time,stop_time,mo_file,sweep_vars=None,fixed_params=[]):
#     initial_factory_for_scen_1 = initialFactoryForWorld3Scenario
#     #Get the mos script factory for a scenario number (valid from 1 to 11)
#     assert 1<=scen_num<=9 , "The scenario number must be between 1 and 9. Your input: {0}".format(scen_num)
#     if sweep_vars or isinstance(sweep_vars,list): #Have to use isinstance for empty lists
#         #If given a list of variables to sweep, don't use defaults
#         final_sweep_vars = sweep_vars
#     else:
#         #If NOT given a list of variables to sweep, use the defaults for that scenario
#         final_sweep_vars = defaultSweepVarsForScenario(scen_num)
#     model_name = world3_settings._world3_scenario_model_skeleton.format(scen_num=scen_num) #global
#     initial_factory_dict = {
#         # "mo_file"     :  world3_settings._sys_dyn_package_pop_state_var_new.replace("\\","/"), #Global
#         "mo_file"     : mo_file,
#         "sweep_vars"  : final_sweep_vars,
#         "model_name"  : model_name,
#         "startTime"   : start_time,
#         "stopTime"    : stop_time,
#         "fixed_params": fixed_params,
#         }
#     initial_factory = mos_script_factory.MosScriptFactory(initial_factory_dict)
#     return initial_factory
# def defaultSweepVarsForScenario(scen_num):
#     default_sweep_vars_dict = defaultSweepVarsDict()
#     return default_sweep_vars_dict[scen_num]
# def defaultSweepVarsDict():
#     default_sweep_vars_dict ={
#             9: ["t_fcaor_time", "t_fert_cont_eff_time", "t_zero_pop_grow_time", "t_ind_equil_time", "t_policy_year", "t_land_life_time"],
#             8: ["t_fcaor_time", "t_fert_cont_eff_time", "t_zero_pop_grow_time", "t_ind_equil_time", "t_policy_year"],
#             7: ["t_fcaor_time", "t_fert_cont_eff_time", "t_zero_pop_grow_time"],
#             6: ["t_fcaor_time", "t_policy_year", "t_land_life_time"],
#             5: ["t_fcaor_time", "t_policy_year", "t_land_life_time"],
#             4: ["t_fcaor_time", "t_policy_year"],
#             3: ["t_fcaor_time", "t_policy_year"],
#             2: ["t_fcaor_time"],
#             1: []
#             }
#     return default_sweep_vars_dict

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
