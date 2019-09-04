#Std
import os
import platform
import logging #en reemplazo de los prints
logger = logging.getLogger("--Run OMC--") #un logger especifico para este modulo

#Mine
import settings.gral_settings as gral_settings
import filesystem.files_aux

def interpreterForCurrentPlatform():
    if platform.system() == "Linux":
        interpreter = gral_settings._interpreter_linux
    elif platform.system() == "Windows":
        interpreter = gral_settings._interpreter_windows
    else:
        logger.error("This script was tested only on Windows and Linux. The omc interpreter for another platform has not been set")
    return interpreter

def runMosScript(script_path):
    script_folder_path = os.path.dirname(script_path)
    #Check if windows or linux:
    interpreter = interpreterForCurrentPlatform()
    command = "{interpreter} {script_path}".format(interpreter=interpreter,script_path=script_path)
    output = filesystem.files_aux.callCMDStringInPath(command,script_folder_path)
    folder_path = os.path.dirname(script_path)
    omc_log_path = os.path.join(folder_path,gral_settings.omc_run_log_filename)
    output_decoded = output.decode("UTF-8")
    writeOMCLog(output_decoded,omc_log_path)

    # TODO: un-comment. Carefully (stdout might be expecting numbers in communicatio with plugin)s
    # logger.debug("OMC Log written to: {omc_log_path}".format(omc_log_path=omc_log_path))
    removeTemporaryFiles(folder_path)
    return output_decoded

def writeOMCLog(log_str, output_path):
    intro_str ="""The following is the output from the OMC script runner from Open Modelica"""+"\n"
    separator_str = 10*"""-"""+"\n"
    final_str = intro_str+separator_str+log_str
    filesystem.files_aux.writeStrToFile(final_str,output_path)
    return 0
def removeTemporaryFiles(folder_path):
    regex = '.*\.(c|o|h|makefile|log|libs|json)$'
    filesystem.files_aux.removeFilesWithRegexAndPath(regex,folder_path)

