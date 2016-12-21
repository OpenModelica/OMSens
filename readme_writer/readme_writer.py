#Imports:
#Standard
import logging #en reemplazo de los prints
logger = logging.getLogger("-- Automatic readme for run writer --") #un logger especifico para este modulo
#Mine:
import settings.gral_settings as gral_settings
import filesystem.files_aux
introduction = "This readme file was automatically generated to ease the effort of understanding the produced outputs. Here you'll find run-specific and run-independant information."


def writeReadme(output_path,sweeping_info):
    logger.debug("Writing readme to path:{output_path}".format(output_path=output_path))
    run_indep_info = runIndependantInformation()
    run_specif_info = runSpecificInformation(sweeping_info)
    final_str = (introduction+"\n\n") + (run_indep_info+"\n\n") + (run_specif_info)
    filesystem.files_aux.writeStrToFile(final_str,output_path)

def runIndependantInformation():
    strs = ["... Information not specific to this run ...",
            omcScriptStr(),
            omcCreationSettingsStr(),
            omcRunLogStr(),
            xmlFileStr(),
            binaryFileStr(),
            csvFilesStr(),
            outOfRangeCasesStr(),
            plotsFolderStr(),]
    return "\n".join(strs)

def plotsFolderStr():
    filename= "plots/<var>"
    explanation = "The plot for the plot_variable (different than the sweep_variables) for each of its values for each iteration."
    return strTemplate(filename,explanation)
def outOfRangeCasesStr():
    filename= "out_of_range_cases.txt"
    explanation = "This file is generated when the interpolation function from SystemDynamics model in OpenModelica is asked to interpolate values outside the default range (lower than the minimum or greater than the maximum). In those cases, we extrapolate linearly outwards the standard interval."
    return strTemplate(filename,explanation)
def csvFilesStr():
    filename= "*.csv files"
    explanation = "This are the results of the sweep. Each .csv corresponds to an iteration. The filenames for this specific run are explained in the 'Run Specific Information' section"
    return strTemplate(filename,explanation)

def binaryFileStr():
    filename= "executable (*.exe in windows. No extension in Linux)"
    explanation = "This is the executable corresponding to the compiled code for the model.  It's used to run each of the experiments for this sweep. It gets it's configuration from the *.xml file."
    return strTemplate(filename,explanation)
def xmlFileStr():
    filename= "*.xml"
    explanation = "This file was automatically generated after compiling the Modelica model and is used by the .mos script to change the experiment conditions for each iteration of the sweep."
    return strTemplate(filename,explanation)

def omcScriptStr():
    filename= gral_settings.mos_script_filename
    explanation = "This file has the OpenModelica Scripting code to be run using omc. It was automatically generated. For example, it will be ran in Linux with the command 'omc {filename}'.".format(filename=filename)
    return strTemplate(filename,explanation)

def omcCreationSettingsStr():
    filename = gral_settings.omc_creation_settings_filename
    explanation = "This file includes the settings with which the OpenModelica script (.mos) was created. This file includes required information to compile and run the simulations, such as the model name, the start and stop time, the variables to be swept, the fixed parameters for each iteration, etc "
    return strTemplate(filename,explanation)

def omcRunLogStr():
    filename = gral_settings.omc_run_log_filename
    explanation = "In this file we dump the stdout output of running the .mos script with omc."
    return strTemplate(filename,explanation)

def strTemplate(filename,explanation):
    return filename+":\n  "+explanation

def runSpecificInformation(sweeping_info):
    strs = ["... Specific info for this run ...",
            sweptVarsStr(sweeping_info["sweep_vars"]),
            iterationsInfo(sweeping_info["per_iter_info_dict"]),
            ]
    return "\n".join(strs)

def sweptVarsStr(swept_vars):
    intro_str = "The script was ran sweeping the following variables (all of them with the same value for each iteration):"
    vars_separated_by_commas = ", ".join(swept_vars)
    return intro_str+"\n  "+vars_separated_by_commas

def iterationsInfo(per_iter_info_dict):
    iterations = len(per_iter_info_dict)
    number_of_iterations_str = "The produced CSV files for the {iterations} values tested are the following:".format(iterations=iterations)
    per_iter_strs= []
    for itera,itera_info in per_iter_info_dict.items():
        iter_num_str = "Iteration number: "+str(itera)
        file_path_str = "  File path:\n    "+itera_info["file_path"]
        sweep_value_str = "  Sweep value:\n   "+str(itera_info["sweep_value"])
        iter_str = "\n".join([iter_num_str,file_path_str,sweep_value_str])
        per_iter_strs.append(iter_str)
    iters_strs = "\n".join(per_iter_strs)
    return number_of_iterations_str+"\n"+iters_strs



