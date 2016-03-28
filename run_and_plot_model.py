#This is the main script for configuring, running and plotting a OpenModelica Sweep
import os
from datetime import datetime
import inspect
import subprocess
import re
import logging #en reemplazo de los prints
import sys
logger = logging.getLogger("--Run and Plot OpenModelica--") #un logger especifico para este modulo
# My imports
import mos_script_factory
import plot_csv

#Funcs for file:
def currentDir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
def parentDir(dir_):
    return os.path.dirname(dir_)
#GLOBALS:
_sys_dyn_package_path = os.path.join(os.path.join(os.path.join(currentDir(),"resource"),"SystemDynamics"),"package.mo")
_world3_scenario_model_skeleton = "SystemDynamics.WorldDynamics.World3.Scenario_{scen_num}"
_plot_var= "population"
# "sweep_vars" has defaults for every scenario!! (but can be overriden passing a list of sweep_vars to initialFactoryForWorld3Scenario
_sweep_vars = [] #CHANGE TO NONE TO USE DEFAULTS!!!!
_initial = 2042
_increment = 10
_iterations=1
_startTime= 1900 #variables used to indicate years to run the simulation (1900 to 2100 for example)
_stopTime= 2500 #variables used to indicate years to run the simulation (1900 to 2100 for example)
_nr_resources_init = 2e12; # std value for scen_1 = 1e12. std value for scen_i for i>1= 2e12 (changes in this global affect only scenarios > 1)
_run_first_scenario = False #if True, it runs the first scenario alone without sweeping anything. If false, it doesn't even run it
_first_scen_to_run = 4 #Always >= than 2 to avoid pointless executing of a non-sweeping scenario
_last_scen_to_run = 4 # Always <= than 9 (even though there are 11 official scenarios)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    #The "root" output folder path.
    output_path = makeOutputPath()
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
    doScenariosSet(scenarios, plot_var=_plot_var,initial=_initial,increment=_increment,iterations=_iterations,output_root_path=output_path )
def doScenariosSet(scenarios,plot_var,initial,increment,iterations,output_root_path):
    for folder_name,initial_scen_factory in scenarios:
        logger.debug("Running scenario {folder_name}".format(folder_name=folder_name))
        os.makedirs(os.path.join(output_root_path,folder_name))
        createSweepRunAndPlotForModelInfo(initial_scen_factory,plot_var=plot_var,initial=initial,increment=increment,iterations=iterations,output_folder_path=os.path.join(output_root_path,folder_name)  )

#CREO QUE DE ACA PARA ABAJO ES INDEPENDIENTE DE WORLD3
def createSweepRunAndPlotForModelInfo(mos_script_factory_inst,plot_var,initial,increment,iterations,output_folder_path):
    # I assume that model dict includes: mo_file, model_name, sweep_vars
    output_mos_path = os.path.join(output_folder_path,"mos_script.mos")
    mos_script_factory_inst.setSetting("plot_var",plot_var)
    mos_script_factory_inst.setSetting("initial",initial)
    mos_script_factory_inst.setSetting("increment",increment)
    mos_script_factory_inst.setSetting("iterations",iterations)
    mos_script_factory_inst.setSetting("output_mos_path",output_mos_path)
    mos_script_factory_inst.writeToFile() #argument-less method for now
    writeRunLog(mos_script_factory_inst.initializedSettings(), os.path.join(output_folder_path,"run_info.txt"))
    runMosScript(output_mos_path)
    #REEMPLAZAR POR EL LOGGER!
    # print("Script path:")
    # print(output_mos_path)
    removeTemporaryFiles(output_folder_path)
    csv_files = csvFiles(output_folder_path)
    plots_folder_path =os.path.join(output_folder_path,"plots")
    os.makedirs(plots_folder_path)
    plot_path = os.path.join(plots_folder_path,plot_var+".svg")
    sweeping_vars = mos_script_factory_inst.initializedSettings()["sweep_vars"]
    plot_title = "Plot for var {plot_var} after sweeping {sweeping_vars_len} vars".format(plot_var=plot_var, sweeping_vars_len= len(sweeping_vars))
    plot_csv.plotVarFromCSVs(plot_var,csv_files,plot_path,plot_title)

def writeRunLog(run_settings_dict, output_path):
    with open(output_path, 'w') as outputFile:
        outputFile.write("""The whole "create mos, run it and plot it" script was run with the following settings"""+"\n")
        outputFile.write("""<setting_name>:\n   <setting_value>"""+"\n")
        outputFile.write("""\n""") #a space between explanation and the important things
        for setting_name,setting_value in run_settings_dict.items():
            setting_str = """{setting_name}:\n {setting_value}""".format(setting_name=setting_name,setting_value=setting_value)
            outputFile.write(setting_str+"\n")
    return 0

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
def world3Scenario2Info():
    scen_dict = world3CommonInfo()
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_2"
    return scen_dict

def world3CommonInfo():
    sys_dyn_path =os.path.join(os.path.join(os.path.join(currentDir(),"resource"),"SystemDynamics"),"package.mo")
    std_dict = {
        "mo_file": sys_dyn_path,
        }
    return std_dict

def csvFiles(folder_path):
    csv_files = []
    for x in os.listdir(folder_path):
        if re.match('.*\.csv$', x):
            csv_files.append(os.path.join(folder_path,x))
    return csv_files

def removeTemporaryFiles(folder_path):
    for x in os.listdir(folder_path):
        if re.match('.*\.(c|o|h|makefile|log|libs|json)$', x):
            os.remove(os.path.join(folder_path,x))

def makeOutputPath():
    dest_path = destPath()
    timestamp_dir = makeDirFromCurrentTimestamp(dest_path)
    return timestamp_dir

def makeDirFromCurrentTimestamp(dest_path):
    logger.debug("Making timestamp dir")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    dateAndTime = datetime.now()
    new_folder_path = os.path.join(dest_path,dateAndTime.strftime('%Y-%m-%d/%H_%M_%S'))
    os.makedirs(new_folder_path)
    return new_folder_path
def destPath():
    tmp_path = tmpPath()
    return os.path.join(tmp_path,"modelica_outputs")
def tmpPath():
    currentdir = currentDir()
    parentdir = parentDir(currentdir)
    # return os.path.join(parentdir,"tmp")
    return os.path.join(currentdir,"tmp")
def runMosScript(script_path):
    # def callMMLWithCFGAndOutputNameToFolderPath(cfg_name,outputName,folder_path):
    script_folder_path = os.path.dirname(script_path)
    command = "{interpreter} {script_path}".format(interpreter="omc",script_path=script_path)
    output = callCMDStringInPath(command,script_folder_path)
    #POR AHORA NO NOS IMPORTA EL OUTPUT EN EL STDOUT:
    folder_path = os.path.dirname(script_path)
    omc_log_path = os.path.join(folder_path,"omc_log.txt")
    output_decoded = output.decode("UTF-8") #en un principio no nos importa el output
    writeOMCLog(output_decoded,omc_log_path)
    logger.debug("OMC Log written to: {omc_log_path}".format(omc_log_path=omc_log_path))
    return output_decoded

def writeOMCLog(log_str, output_path):
    with open(output_path, 'w') as outputFile:
        outputFile.write("""The following is the output from the OMC script runner from Open Modelica"""+"\n")
        outputFile.write(10*"""-"""+"\n")
        outputFile.write(log_str)
        return 0

def callCMDStringInPath(command,path):
    process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True,cwd=path)
    output = process.communicate()[0]
    return output

if __name__ == "__main__":
    main()

