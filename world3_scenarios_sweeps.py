import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--World3 scenarios sweep--") #un logger especifico para este modulo
# Mine:
import mos_script_factory
import run_and_plot_model
import files_aux

#Aux for GLOBALS:
## Skeletons of sweep_value_formula_str. Free variable: i (goes from 0 to (iterations-1) ):
_increasing_by_increment_from_initial_skeleton = "{initial} + i*{increment}"
_increasing_by_percentage_from_initial_skeleton = "{initial}*({percentage}/100*i+1)"
def deltaBeforeAndAfter(p,iterations,delta): #Have to create a function for "delta_before_and_after" because I have to convert to int in python and not in the Modelica Scripting Language
    iterations_div_2_int = int(iterations/2)
    return "{p}*(1-{iterations_div_2_int}*{delta}) + {p}*({delta}*i)".format(p=p,iterations_div_2_int=iterations_div_2_int,delta=delta)
## Examples:
# sweep_value_formula_str = _increasing_by_increment_from_initial_skeleton.format(initial=2012,increment=10) # "2012 + i*10" --> 2012,2022,2032...
# sweep_value_formula_str = _increasing_by_percentage_from_initial_skeleton.format(initial=1e12,percentage=20) # "1e12*((20/100)*i+1)" --> 1e12, 1.2e12, 1.4e12 ...
# sweep_value_formula_str = deltaBeforeAndAfter(p=10,delta=0.01,iterations=_iterations) # '10*(1-3*0.01) + 10*(0.01*i)' --> 9.7, 9.8, 9.9, 10, 10.1 ....

##### GLOBALS: #####
_sys_dyn_package_path = os.path.join(os.path.join(os.path.join(files_aux.currentDir(),"resource"),"SystemDynamics"),"package.mo")
_world3_scenario_model_skeleton = "SystemDynamics.WorldDynamics.World3.Scenario_{scen_num}"
_plot_var= "population"
_startTime= 1900 # year to start the simulation (1900 example)
_stopTime= 2500  # year to end the simulation (2100 for example)
_scens_to_run = [1,2,3,4,5,6,7,8,9] #List of ints representing the scenarios to run (from 1 to 11).  Example: [1,2,3,4,5,6,7,8,9]

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    testYears()
    testDeltaNRResources()

## Predefined tests
def testDeltaNRResources():
    iterations = 10
# "sweep_vars" has defaults for scenarios 1 to 9!! (but can be overriden passing a list of sweep_vars to initialFactoryForWorld3Scenario)
    sweep_vars= ["nr_resources_init"] # Set to None to use scenario specific defaults (year of application of policies). Examples: None, ["nr_resources_init"]
    sweep_value_formula_str = deltaBeforeAndAfter(p=1e12,delta=0.1,iterations=iterations) #Has to be a string with only free variable "i"
    fixed_params = []  # Params changes that will be fixed throughout the sweep. Example: [("nr_resources_init",2e12)]
    setUpSweepsAndRun(iterations,sweep_vars,sweep_value_formula_str,fixed_params)

def testYears():
    iterations = 6
# "sweep_vars" has defaults for scenarios 1 to 9!! (but can be overriden passing a list of sweep_vars to initialFactoryForWorld3Scenario)
    sweep_vars= None # Set to None to use scenario specific defaults (year of application of policies). Examples: None, ["nr_resources_init"]
    sweep_value_formula_str = _increasing_by_increment_from_initial_skeleton.format(initial=2012,increment=10) # "2012 + i*10" --> 2012,2022,2032...
    fixed_params = []  # Params changes that will be fixed throughout the sweep. Example: [("nr_resources_init",2e12)]
    setUpSweepsAndRun(iterations,sweep_vars,sweep_value_formula_str,fixed_params)

#World3 specific:
def setUpSweepsAndRun(iterations,sweep_vars,sweep_value_formula_str,fixed_params):
    #The "root" output folder path.
    output_path = files_aux.makeOutputPath()
    #Create scenarios from factory
    scenarios = []
    for i in _scens_to_run:
        initial_factory_for_scen_i = initialFactoryForWorld3Scenario(scen_num=i,start_time=_startTime,stop_time=_stopTime,fixed_params=fixed_params,sweep_vars=sweep_vars)
        scenario_tuple =("scenario_"+str(i),initial_factory_for_scen_i)
        scenarios.append(scenario_tuple)
    doScenariosSet(scenarios, plot_var=_plot_var,iterations=iterations,output_root_path=output_path, sweep_value_formula_str=sweep_value_formula_str)
def doScenariosSet(scenarios,plot_var,iterations,output_root_path,sweep_value_formula_str):
    for folder_name,initial_scen_factory in scenarios:
        logger.debug("Running scenario {folder_name}".format(folder_name=folder_name))
        os.makedirs(os.path.join(output_root_path,folder_name))
        run_and_plot_model.createSweepRunAndPlotForModelInfo(initial_scen_factory,plot_var=plot_var,iterations=iterations,output_folder_path=os.path.join(output_root_path,folder_name),sweep_value_formula_str=sweep_value_formula_str  )
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
