#This is the main script for configuring, running and plotting a OpenModelica Sweep
# 1) Set up run:
#    a) Get .mo
#    b) get initial configuration (standard config)
#    c) get new parameters (parameters that differ from the standard)
#    d) Choose between .mos script or OMPython:
#       A) .mos:
#          A.1) Create output folder (recycle "timestamp dir" from MML_Extra_Scripts)
#          A.2) Create .mos file in output folder from .mos skeleton that includes the following:
#               A.3.1) Build model: this will create a binary and a .xml file.
#                      A.3.1.Alternate.1) If the model doesn't include an initial configuration and no .xml
#                        file was created, create one yourself from 1.b).
#                      A.3.Alternate.2) If the .xml file has the initial configuration from 1.b), then just
#                        use it and don't do anything.
#               A.3.2) Set the new parameters from 1.c) to the .xml file and run it
#               A.3.3) repeat A.3.2) for all the sets of parameters.
#         A.3) Run the .mos file with command omc
#         A.4) Delete all the {model_name}* temporary files created by the build
#       B) Very similar to A) but "live" with process comunication using OMPYthon instead of
#          creating a .mos file
#   e) Plot using python or OMPlot:
#      A) Python:
#         A.1) Get all the csv files and the variables to plot for each experiment
#         A.2) Setup pyplot
#         A.3) Get the data for a .csv using np
#         A.4) plot using the variable to choose the column from the data, "variable_file" as label
#              and column "time" as x axis
#         A.5) repeat A.4) for all the variables
#         A.6) repeat A.3)-A.5) for all the csvs
#      B) OMPlot:
#        a) Read Adeel's new mail and find out how to plot multiple experiments from the same model
#           in the same plot
import os
from datetime import datetime
import inspect
import subprocess
import re
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
_initial = 2012
_increment = 10
_iterations=5
_startTime= 1900 #variables used to indicate years to run the simulation (1900 to 2100 for example)
_stopTime= 2500 #variables used to indicate years to run the simulation (1900 to 2100 for example)


import logging #en reemplazo de los prints
logger = logging.getLogger("--Run and Plot OpenModelica--") #un logger especifico para este modulo

def main():
    #The "root" output folder path.
    output_path = makeOutputPath()
    #First run scenario 1 without sweeping anything and with 1 iteration (we use it as a base to compare):
    initial_factory_for_scen_1 = initialFactoryForWorld3Scenario(scen_num=1,start_time=_startTime,stop_time=_stopTime)
    doScenariosSet([("scenario_1",initial_factory_for_scen_1)], plot_var=_plot_var,initial=_initial,increment=_increment,iterations=1,output_root_path=output_path )
    #Create scenarios from factory
    scenarios = []
    # for i in range(2,10):
    for i in range(3,4):
        initial_factory_for_scen_i = initialFactoryForWorld3Scenario(scen_num=i,start_time=_startTime,stop_time=_stopTime)
        scenario_tuple =("scenario_"+str(i),initial_factory_for_scen_i)

        scenarios.append(scenario_tuple)
    doScenariosSet(scenarios, plot_var=_plot_var,initial=_initial,increment=_increment,iterations=_iterations,output_root_path=output_path )
def doScenariosSet(scenarios,plot_var,initial,increment,iterations,output_root_path):
    for folder_name,initial_scen_factory in scenarios:
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
    runMosScript(output_mos_path)
    print("Script path:")
    print(output_mos_path)
    removeTemporaryFiles(output_folder_path)
    csv_files = csvFiles(output_folder_path)
    plots_folder_path =os.path.join(output_folder_path,"plots")
    os.makedirs(plots_folder_path)
    plot_path = os.path.join(plots_folder_path,plot_var+".svg")
    print(mos_script_factory_inst.initializedSettings())
    sweeping_vars = mos_script_factory_inst.initializedSettings()["sweep_vars"]
    plot_title = "Plot for var {plot_var} after sweeping {sweeping_vars_len} vars".format(plot_var=plot_var, sweeping_vars_len= len(sweeping_vars))
    plot_csv.plotVarFromCSVs(plot_var,csv_files,plot_path,plot_title)

# if iscenario == 4 then
# SET_t_fcaor_time		= changeyear ;
# SET_t_policy_year		= changeyear ;
# SET_nr_resources_init = 2e12; // As in all scenarios other than 1
# end if;

def initialFactoryForWorld3Scenario(scen_num,start_time,stop_time,sweep_vars=None):
    initial_factory_for_scen_1 = initialFactoryForWorld3Scenario
    #Get the mos script factory for a scenario number (valid from 1 to 11)
    assert 1<=scen_num<=9 , "The scenario number must be between 1 and 9. Your input: {0}".format(scen_num)
    if sweep_vars:
        #If given a list of variables to sweep, don't use defaults
        final_sweep_vars = sweep_vars
    else:
        #If NOT given a list of variables to sweep, use the defaults for that scenario
        final_sweep_vars = defaultSweepVarsForScenario(scen_num)
    model_name = _world3_scenario_model_skeleton.format(scen_num=scen_num) #global
    initial_factory_dict = {
        "mo_file": _sys_dyn_package_path, #Global
        "sweep_vars": final_sweep_vars,
        "model_name": model_name,
        "startTime" : start_time,
        "stopTime"  : stop_time
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
    output_decoded = output.decode("UTF-8") #en un principio no nos importa el output
    print(output_decoded)
    return output_decoded


def callCMDStringInPath(command,path):
    process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True,cwd=path)
    output = process.communicate()[0]
    return output

if __name__ == "__main__":
    main()

