#This is the main script for configuring, running and plotting a OpenModelica Sweep
import os
import subprocess
import re
import logging #en reemplazo de los prints
logger = logging.getLogger("--Run and Plot OpenModelica--") #un logger especifico para este modulo
# My imports
import plot_csv

def createSweepRunAndPlotForModelInfo(mos_script_factory_inst,plot_var,initial,increment,iterations,output_folder_path,sweep_value_formula_skeleton):
    output_mos_path = os.path.join(output_folder_path,"mos_script.mos")
    mos_script_factory_inst.setSetting("plot_var",plot_var)
    mos_script_factory_inst.setSetting("initial",initial)
    mos_script_factory_inst.setSetting("increment",increment)
    mos_script_factory_inst.setSetting("iterations",iterations)
    mos_script_factory_inst.setSetting("sweep_value_formula_skeleton",sweep_value_formula_skeleton)
    mos_script_factory_inst.setSetting("output_mos_path",output_mos_path)
    mos_script_factory_inst.writeToFile() #argument-less method for now
    writeRunLog(mos_script_factory_inst.initializedSettings(), os.path.join(output_folder_path,"run_info.txt"))
    runMosScript(output_mos_path)
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
    command = "{interpreter} {script_path}".format(interpreter="omc",script_path=script_path)
    output = callCMDStringInPath(command,script_folder_path)
    folder_path = os.path.dirname(script_path)
    omc_log_path = os.path.join(folder_path,"omc_log.txt")
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


