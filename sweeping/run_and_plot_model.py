#This is the main script for configuring, running and plotting a OpenModelica Sweep
import os
import subprocess
import re
import platform
import logging #en reemplazo de los prints
logger = logging.getLogger("--Run and Plot OpenModelica--") #un logger especifico para este modulo
# My imports
import plotting.plot_csv as plot_csv
import settings.gral_settings as gral_settings

#Globals:
_interpreter_windows= "%OPENMODELICAHOME%\\bin\\omc"
_interpreter_linux = "omc"

def createSweepRunAndPlotForModelInfo(mos_script_factory_inst,plot_var,iterations,output_folder_path,sweep_value_formula_str,csv_file_name_python_skeleton,csv_file_name_modelica_skeleton):
    output_mos_path = os.path.join(output_folder_path,gral_settings.mos_script_filename)
	# EL scripting de modelica se rompe con la backslash (aunque estemos en windows). Hay que mandar la de unix nomas:
    output_mos_path = output_mos_path.replace("\\","/")
    csv_file_name_modelica = csv_file_name_modelica_skeleton.format(**{})
    mos_script_factory_inst.setSetting("csv_file_name_modelica",csv_file_name_modelica)
    mos_script_factory_inst.setSetting("plot_var",plot_var)
    mos_script_factory_inst.setSetting("iterations",iterations)
    mos_script_factory_inst.setSetting("sweep_value_formula_str",sweep_value_formula_str)
    mos_script_factory_inst.setSetting("output_mos_path",output_mos_path)
    mos_script_factory_inst.createMosScript() #argument-less method for now
    writeRunLog(mos_script_factory_inst.initializedSettings(), os.path.join(output_folder_path,gral_settings.omc_creation_settings_filename))
    runMosScript(output_mos_path)
    removeTemporaryFiles(output_folder_path)
    # csv_files = csvFiles(output_folder_path)
    plots_folder_path =os.path.join(output_folder_path,"plots")
    os.makedirs(plots_folder_path)
    plot_path_without_extension = os.path.join(plots_folder_path,plot_var)
    sweeping_vars = mos_script_factory_inst.initializedSettings()["sweep_vars"]
    # plot_title = "Plot for var {plot_var} after sweeping {sweeping_vars_len} vars".format(plot_var=plot_var, sweeping_vars_len= len(sweeping_vars))
    # plot_csv.plotVarFromCSVs(plot_var,csv_files,plot_path,plot_title)
    sweeping_info = sweepingInfoPerIteration(mos_script_factory_inst.initializedSettings(),csv_file_name_python_skeleton)
    model_name_only = mos_script_factory_inst.initializedSettings()["model_name"].split(".")[-1]
    plot_csv.plotVarFromSweepingInfo(plot_var,model_name_only,sweeping_info,plot_path_without_extension)

def sweepingInfoPerIteration(settings,csv_file_name_python_skeleton):
    iterations                = settings["iterations"]
    sweep_formula             = settings["sweep_value_formula_str"] #only variable should be i
    model_name                = settings["model_name"]
    output_mos_path           = settings["output_mos_path"]
    run_root_folder = os.path.dirname(output_mos_path)
    sweep_vars = settings["sweep_vars"]
    per_iter_info_dict = {}
    for i in range(0,iterations):
        iter_dict = {}
        csv_name = csv_file_name_python_skeleton.format(**{"model_name":model_name,"i_str":str(i)})
        csv_path = os.path.join(run_root_folder,csv_name)
        iter_dict["file_path"]   = csv_path
        iter_dict["sweep_value"] = eval(sweep_formula) # this eval uses i!!!
        per_iter_info_dict[i] = iter_dict
    sweeping_info_dict = {}
    sweeping_info_dict["per_iter_info_dict"] = per_iter_info_dict
    sweeping_info_dict["sweep_vars"] = sweep_vars
    return sweeping_info_dict

def writeRunLog(run_settings_dict, output_path):
    with open(output_path, 'w') as outputFile:
        outputFile.write("""The whole "create mos, run it and plot it" script was run with the following settings"""+"\n")
        outputFile.write("""<setting_name>:\n   <setting_value>"""+"\n")
        outputFile.write("""\n""") #a space between explanation and the important things
        for setting_name,setting_value in run_settings_dict.items():
            setting_str = """{setting_name}:\n {setting_value}""".format(setting_name=setting_name,setting_value=setting_value)
            outputFile.write(setting_str+"\n")
    return 0

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

def runMosScript(script_path):
    script_folder_path = os.path.dirname(script_path)
    #Check if windows or linux:
    if platform.system() == "Linux":
        interpreter = _interpreter_linux
    elif platform.system() == "Windows":
        interpreter = _interpreter_windows
    else:
        logger.error("This script was tested only on Windows and Linux. The omc interpreter for another platform has not been set")

    command = "{interpreter} {script_path}".format(interpreter=interpreter,script_path=script_path)
    output = callCMDStringInPath(command,script_folder_path)
    folder_path = os.path.dirname(script_path)
    omc_log_path = os.path.join(folder_path,gral_settings.omc_run_log_filename)
    output_decoded = output.decode("UTF-8")
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


