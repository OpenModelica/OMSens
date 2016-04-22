import settings.gral_settings as gral_settings
introduction = "This readme file was automatically generated to ease the effort of understanding the produced outputs. Here you'll find run-specific and run-independant information."
def writeReadme(output_path):
    run_indep_info = runIndependantInformation()
    with open(output_path, 'w') as outputFile:
        outputFile.write(introduction+"\n\n")
        outputFile.write(run_indep_info)

def runIndependantInformation():
    strs = ["... Information not specific to this run ...",
            omcScriptStr(),
            omcCreationSettingsStr(),
            omcRunLogStr(),
            xmlFileStr(),
            binaryFileStr(),
            csvFilesStr(),]
    return "\n".join(strs)

def csvFilesStr():
    filename= "*.csv files"
    explanation = "This are the results of the sweep. Each .csv correspond to an iteration. The filenames for this specific run are explained in the 'Run Specific Information' section"
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
    explanation = "This file has the OpenModelica Scripting code to be run using omc. It was automatically generated."
    return strTemplate(filename,explanation)

def omcCreationSettingsStr():
    filename = gral_settings.omc_creation_settings_filename
    explanation = "This file includes the settings with which the OpenModelica script (.mos) was created. This file includes required information to compile and run the simulations, such as the model name, the start and stop time, etc. "
    return strTemplate(filename,explanation)

def omcRunLogStr():
    filename = gral_settings.omc_run_log_filename
    explanation = "In this file we dump the stdout output of running the .mos script with omc."
    return strTemplate(filename,explanation)

def strTemplate(filename,explanation):
    return filename+":\n  "+explanation

