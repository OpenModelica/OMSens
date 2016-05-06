import settings.gral_settings as gral_settings
introduction = "This readme file was automatically generated to ease the effort of understanding the produced outputs. Here you'll find run-specific and run-independant information."


##BORRA DESDE ACA
sweeping_info_asd ={'sweep_vars': ['t_fcaor_time', 't_fert_cont_eff_time', 't_zero_pop_grow_time', 't_ind_equil_time',
    't_policy_year', 't_land_life_time'], 'per_iter_info_dict': {0: {'file_path':
        '/home/adanos/Documents/TPs/tesis/repos/modelica_scripts/tmp/modelica_outputs/2016-04-23/02_01_13/scenario_9/iter_0.csv',
        'sweep_value': 2012}, 1: {'file_path':
            '/home/adanos/Documents/TPs/tesis/repos/modelica_scripts/tmp/modelica_outputs/2016-04-23/02_01_13/scenario_9/iter_1.csv',
            'sweep_value': 2022}}}
## BORRA HASTA ACA

def writeReadme(output_path,sweeping_info):
    run_indep_info = runIndependantInformation()
    run_specif_info = runSpecificInformation(sweeping_info)
    with open(output_path, 'w') as outputFile:
        outputFile.write(introduction+"\n\n")
        outputFile.write(run_indep_info+"\n\n")
        outputFile.write(run_specif_info)

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



