import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--World3 scenarios sweep--") #un logger especifico para este modulo
# Mine:
import mos_script_factory
import run_and_plot_model
import files_aux

#GLOBALS:
_sys_dyn_package_path = os.path.join(os.path.join(os.path.join(files_aux.currentDir(),"resource"),"SystemDynamics"),"package.mo")
_world3_scenario_model_skeleton = "SystemDynamics.WorldDynamics.World3.Scenario_{scen_num}"
_plot_var= "population"
# "sweep_vars" has defaults for every scenario!! (but can be overriden passing a list of sweep_vars to initialFactoryForWorld3Scenario
_sweep_vars = None #CHANGE TO NONE TO USE DEFAULTS!!!!
_initial = 2012
_increment = 10
_iterations=3
_sweep_value_formula_skeleton = "{d[initial]} + i*{d[increment]}" #Example: "{d[initial]} + i*{d[increment]}". Using "d[x]" instead of just "x" is mandatory because of python's lack of better options. i is fixed by the for inside the .mos script and is the variable that increases from 0 to iterations-1 by 1
_startTime= 1900 #variables used to indicate years to run the simulation (1900 to 2100 for example)
_stopTime= 2500 #variables used to indicate years to run the simulation (1900 to 2100 for example)
_nr_resources_init = 2e12; # std value for scen_1 = 1e12. std value for scen_i for i>1= 2e12 (changes in this global affect only scenarios > 1)
_run_first_scenario = False #if True, it runs the first scenario alone without sweeping anything. If false, it doesn't even run it
_first_scen_to_run = 4 #Always >= than 2 to avoid pointless executing of a non-sweeping scenario
_last_scen_to_run = 4 # Always <= than 9 (even though there are 11 official scenarios)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    #The "root" output folder path.
    output_path = files_aux.makeOutputPath()
    #Fixed parameter changes for all the runs:
    #First run scenario 1 without sweeping anything and with 1 iteration (we use it as a base to compare):
    if _run_first_scenario:
        logger.debug("Running first scenario")
        fixed_params = [] #No fixed changes for scenario 1
        initial_factory_for_scen_1 = initialFactoryForWorld3Scenario(scen_num=1,start_time=_startTime,stop_time=_stopTime,fixed_params=fixed_params)
        doScenariosSet([("scenario_1",initial_factory_for_scen_1)], plot_var=_plot_var,initial=_initial,increment=_increment,iterations=1,output_root_path=output_path )
    #Create scenarios from factory
    scenarios = []
    for i in range(_first_scen_to_run,_last_scen_to_run+1):
        fixed_params = [("nr_resources_init",_nr_resources_init)] #available resources doubled for scenarios later than 1
        initial_factory_for_scen_i = initialFactoryForWorld3Scenario(scen_num=i,start_time=_startTime,stop_time=_stopTime,fixed_params=fixed_params,sweep_vars=_sweep_vars)
        scenario_tuple =("scenario_"+str(i),initial_factory_for_scen_i)

        scenarios.append(scenario_tuple)
    doScenariosSet(scenarios, plot_var=_plot_var,initial=_initial,increment=_increment,iterations=_iterations,output_root_path=output_path, sweep_value_formula_skeleton=_sweep_value_formula_skeleton)

#World3 specific:
def doScenariosSet(scenarios,plot_var,initial,increment,iterations,output_root_path,sweep_value_formula_skeleton=_sweep_value_formula_skeleton):
    for folder_name,initial_scen_factory in scenarios:
        logger.debug("Running scenario {folder_name}".format(folder_name=folder_name))
        os.makedirs(os.path.join(output_root_path,folder_name))
        run_and_plot_model.createSweepRunAndPlotForModelInfo(initial_scen_factory,plot_var=plot_var,initial=initial,increment=increment,iterations=iterations,output_folder_path=os.path.join(output_root_path,folder_name),sweep_value_formula_skeleton=sweep_value_formula_skeleton  )
def initialFactoryForWorld3Scenario(scen_num,start_time,stop_time,sweep_vars=None,fixed_params=[]):
    initial_factory_for_scen_1 = initialFactoryForWorld3Scenario
    #Get the mos script factory for a scenario number (valid from 1 to 11)
    assert 1<=scen_num<=9 , "The scenario number must be between 1 and 9. Your input: {0}".format(scen_num)
    if sweep_vars or isinstance(sweep_vars,list): #Have to use isinstance for empty lists
        #If given a list of variables to sweep, don't use defaults
        final_sweep_vars = sweep_vars
    else:
        #If NOT given a list of variables to sweep, use the defaults for that scenario
        final_sweep_vars = defaultSweepVarsForScenario(scen_num)
    model_name = _world3_scenario_model_skeleton.format(scen_num=scen_num) #global
    initial_factory_dict = {
        "mo_file"     : _sys_dyn_package_path, #Global
        "sweep_vars"  : final_sweep_vars,
        "model_name"  : model_name,
        "startTime"   : start_time,
        "stopTime"    : stop_time,
        "fixed_params": fixed_params,
        }
    initial_factory = mos_script_factory.MosScriptFactory(initial_factory_dict)
    return initial_factory
def defaultSweepVarsForScenario(scen_num):
    default_sweep_vars_dict = defaultSweepVarsDict()
    return default_sweep_vars_dict[scen_num]
def defaultSweepVarsDict():
    default_sweep_vars_dict ={
            9: ["t_fcaor_time", "t_fert_cont_eff_time", "t_zero_pop_grow_time", "t_ind_equil_time", "t_policy_year", "t_land_life_time"],
            8: ["t_fcaor_time", "t_fert_cont_eff_time", "t_zero_pop_grow_time", "t_ind_equil_time", "t_policy_year"],
            7: ["t_fcaor_time", "t_fert_cont_eff_time", "t_zero_pop_grow_time"],
            6: ["t_fcaor_time", "t_policy_year", "t_land_life_time"],
            5: ["t_fcaor_time", "t_policy_year", "t_land_life_time"],
            4: ["t_fcaor_time", "t_policy_year"],
            3: ["t_fcaor_time", "t_policy_year"],
            2: ["t_fcaor_time"],
            1: []
            }
    return default_sweep_vars_dict

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
