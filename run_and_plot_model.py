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
import sweeping_mos_creator as swe_mos_creat
import plot_csv


import logging #en reemplazo de los prints
logger = logging.getLogger("--Run and Plot OpenModelica--") #un logger especifico para este modulo

def main():
    output_path = makeOutputPath()
    # scenarios = [("scenario_2",world3Scenario2Info())]
    scenarios = [("scenario_2",world3Scenario2Info()),
                 ("scenario_3",world3Scenario3Info()),
                 ("scenario_4",world3Scenario4Info()),
                 ("scenario_5",world3Scenario5Info()),
                 ("scenario_6",world3Scenario6Info()),
                 ("scenario_7",world3Scenario7Info()),
                 ("scenario_8",world3Scenario8Info()),
                 ("scenario_9",world3Scenario9Info()),
                 ]
    #
    doScenariosSet(scenarios, plot_var="population",initial=2002,increment=1,iterations=10,output_root_path=output_path )
def doScenariosSet(scenarios,plot_var,initial,increment,iterations,output_root_path):
    for folder_name,scenario_dict in scenarios:
        os.makedirs(os.path.join(output_root_path,folder_name))
        createSweepRunAndPlotForModelInfo(scenario_dict,plot_var=plot_var,initial=initial,increment=increment,iterations=iterations,output_folder_path=os.path.join(output_root_path,folder_name)  )

def createSweepRunAndPlotForModelInfo(model_dict,plot_var,initial,increment,iterations,output_folder_path):
    # I assume that model dict includes: mo_file, model_name, sweep_vars
    mos_dict = model_dict.copy()
    mos_dict["plot_var"] = plot_var
    mos_dict["initial"] = initial
    mos_dict["increment"] = increment
    mos_dict["iterations"] = iterations
    mos_dict["output_mos_path"] = os.path.join(output_folder_path,"mos_script.mos")

#     create_mos_kwargs = {
#         # "mo_file":os.path.join(os.path.join(currentDir(),"resource"),"BouncingBall.mo"),
#         "mo_file": sys_dyn_path,
#         # "model_name": "BouncingBall",
#         "model_name": "SystemDynamics.WorldDynamics.World3.Scenario_1",
#         # "sweep_var": "h",
#         # "sweep_var": "t_fcaor_time",
# # SET_t_policy_year       = changeyear ;
#         "sweep_var": "life_expect_norm",
#         # "plot_var": "h",
#         "plot_var": "nr_resources",
#         # "initial": 0.7,
#         "initial": 25,
#         # "increment": 0.1,
#         "increment": 1,
#         # "iterations": 3,
#         "iterations": 10,
#         "output_mos_path": os.path.join(output_path,"bball_sweep.mos"),
#         }
    swe_mos_creat.createMos(**mos_dict)
    runMosScript(mos_dict["output_mos_path"])
    print("Script path:")
    print(mos_dict["output_mos_path"])
    removeTemporaryFiles(output_folder_path,mos_dict["model_name"])
    csv_files = csvFiles(output_folder_path)
    plots_folder_path =os.path.join(output_folder_path,"plots")
    os.makedirs(plots_folder_path)
    plot_path = os.path.join(plots_folder_path,plot_var+".svg")
    plot_csv.plotVarFromCSVs(plot_var,csv_files,plot_path)

# if iscenario == 4 then
# SET_t_fcaor_time		= changeyear ;
# SET_t_policy_year		= changeyear ;
# SET_nr_resources_init = 2e12; // As in all scenarios other than 1
# end if;

def world3Scenario9Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time",
        "t_fert_cont_eff_time",
        "t_ind_equil_time",
        "t_land_life_time",
        "t_policy_year",
        "t_zero_pop_grow_time"]
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_9"
    return scen_dict

def world3Scenario8Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time",
        "t_fert_cont_eff_time",
        "t_ind_equil_time",
        "t_policy_year",
        "t_zero_pop_grow_time"]
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_8"
    return scen_dict
def world3Scenario7Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time",
        "t_fert_cont_eff_time",
        "t_zero_pop_grow_time"]
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_7"
    return scen_dict
def world3Scenario6Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time",
        "t_land_life_time",
        "t_policy_year"]
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_6"
    return scen_dict
def world3Scenario5Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time",
        "t_land_life_time",
        "t_policy_year"]
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_5"
    return scen_dict
def world3Scenario4Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time", "t_policy_year"]
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_4"
    return scen_dict
def world3Scenario3Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time","t_policy_year"]
    scen_dict["model_name"] = "SystemDynamics.WorldDynamics.World3.Scenario_3"
    return scen_dict
def world3Scenario2Info():
    scen_dict = world3CommonInfo()
    scen_dict["sweep_vars"] = ["t_fcaor_time"]
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

def removeTemporaryFiles(folder_path,name_prefix):
    for x in os.listdir(folder_path):
        if re.match(name_prefix+'.*\.(c|o|h|makefile|log|libs|xml|json)$', x):
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
def currentDir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
def parentDir(dir_):
    return os.path.dirname(dir_)
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

