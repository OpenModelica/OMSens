# Std
import json
import logging
import os
import platform

# Mine
import filesystem.files_aux as files_aux
import settings.gral_settings

logger = logging.getLogger("--SensMosWriter--")  # this modules logger

# Posibles lv para el omc_logger:
# LOG_DEBUG: shows all .xml read values (3k lines)
# LOG_SOLVER: show jacobian matrix info
# omc_logger_flags = "-w -lv=LOG_SOLVER"
# omc_logger_flags = "-w"
omc_logger_flags = ""


def createMosFromJSON(json_file_path, output_mos_path, std_run_filename):
    # Read json
    full_json = readJSON(json_file_path)
    mos_creator_kwargs = mosCreationArgsFromJSON(full_json, output_mos_path, std_run_filename)
    createMos(**mos_creator_kwargs)
    # TODO: The following results should be returned by the "createMos" function but it needs to be reified first
    #   cont. of TODO: This works until we change the assumed convention inside createMos.
    # TODO: It should also be an object named "MosScriptResults" or something of the sort.
    mos_script_params_info_dict = {}
    # Get the function that we use to have a convention of CSV names for perturbed parameters simulations results.
    #  TODO: This function should be removed in the future in favor of just chossing a file name in this function and
    #   cont. of TODO:  returning it.
    csv_file_name_modelica_function = settings.gral_settings.calc_sens_csv_file_name_function
    # Get the path of the mos script to be created so we can return the path to the simulation results instead of just
    #   their filenames.
    mos_folder_path = os.path.dirname(output_mos_path)
    percentage = full_json["percentage"]
    for param_perturb_specs in full_json["params_info_list"]:
        # Gather perturbation specs for this param
        param_name = param_perturb_specs["name"]
        initial_val = param_perturb_specs["initial_val"]
        # Create param info dict for output
        param_info_in_mos = {
            "simu_file_path": os.path.join(mos_folder_path,csv_file_name_modelica_function(param_name)),
            "std_val": initial_val,
            "perturbed_val": initial_val * (1 + percentage / 100),
        }
        # Add param info for this param to the dict with all params infos
        mos_script_params_info_dict[param_name] = param_info_in_mos
    mos_script_info_dict = {
        "perturbed_runs": mos_script_params_info_dict,
        # TODO: The filename should be output of the mos creator function. It shouldn't be an input.
        "std_run_file_name": std_run_filename,
    }
    return mos_script_info_dict


def mosCreationArgsFromJSON(full_json, output_mos_path, std_run_filename):
    mo_file_path = moFilePathFromJSONMoPath(full_json["model_mo_path"])
    # Set .mos creator arguments
    mos_creator_kwargs = {
        "model_name": full_json["model_name"],
        "mo_file": mo_file_path,
        "startTime": full_json["start_time"],
        "stopTime": full_json["stop_time"],
        "params_info_list": full_json["params_info_list"],
        "percentage": full_json["percentage"],
        "output_mos_path": output_mos_path,
        "csv_file_name_modelica_function": settings.gral_settings.calc_sens_csv_file_name_function,
        "std_run_filename": std_run_filename,
    }
    return mos_creator_kwargs


def moFilePathFromJSONMoPath(json_mo_path):
    # Check if it's absolute path or relative path and act accordingly
    is_abs_path = os.path.isabs(json_mo_path)
    if is_abs_path:
        # If it's already an absolute path, there's nothing to do
        mo_file_path = json_mo_path
    else:
        # If it's a relative path, make it absolute
        mo_file_path = os.path.abspath(json_mo_path)
    return mo_file_path


def readJSON(json_file_path):
    with open(json_file_path, 'r') as fp:
        full_json = json.load(fp)
    return full_json


def createMos(mo_file, model_name, params_info_list, percentage, output_mos_path, startTime, stopTime,
              csv_file_name_modelica_function, std_run_filename=None):
    # Create mos script that is OMC compatible
    load_and_build_str = strForLoadingAndBuilding(mo_file, model_name, startTime, stopTime)
    run_std_run_str = strStandardRun(model_name, std_run_filename)
    perturbate_param_and_run_str = strForPerturbateParamAndRun(params_info_list, model_name, percentage,
                                                               csv_file_name_modelica_function, omc_logger_flags)

    # Join the different strs into one
    final_str = load_and_build_str + run_std_run_str + perturbate_param_and_run_str
    # Write final string to file
    files_aux.writeStrToFile(final_str, output_mos_path)
    return 0


def strStandardRun(model_name, std_run_filename):
    if std_run_filename:
        # If we need to run the standard run alongside the other simulations:
        run_std_run_str = strForRunStdRun(model_name, std_run_filename, omc_logger_flags)
    else:
        # If no std run needs to be run, just put it's str as empty
        run_std_run_str = ""
    return run_std_run_str


def strForRunStdRun(model_name, std_run_filename, omc_logger_flags):
    # Human readable comment in resulting .mos
    comment_tag_str = "\n// Running standard run (no parameters modified)"
    # Define lambda for simulation filename so that the file name is fixed
    lambda_ignore_param_name = lambda param_name, std_run_filename=std_run_filename: std_run_filename
    # Simulation file name
    filename_and_cmd_defs_str = strForFilenameAndCmdDefs(lambda_ignore_param_name, "", model_name, omc_logger_flags)
    # Simulate without perturbing any parameter
    run_cmd_str = "\n" + run_system_command_str + "\n"
    # Join the above strs into one
    run_std_run_str = comment_tag_str + filename_and_cmd_defs_str + run_cmd_str
    return run_std_run_str


def strForPerturbateParamAndRun(params_info_list, model_name, percentage, csv_file_name_modelica_function,
                                omc_logger_flags):
    temp_str = ""
    # Get the strings for all but the last parameter
    for i in range(len(params_info_list) - 1):
        pos = i
        include_param_val_rollback = True
        this_param_str = strForParamPerturbationForParamInPosition(
            csv_file_name_modelica_function, include_param_val_rollback, model_name, omc_logger_flags, params_info_list,
            percentage, pos)
        temp_str = temp_str + this_param_str
    # Make the string of the last parameter on its own so we don't add a "setInitXML" at the end which obfuscates the
    # last output of the script run
    pos = -1
    include_param_val_rollback = False
    this_param_str = strForParamPerturbationForParamInPosition(
        csv_file_name_modelica_function, include_param_val_rollback, model_name, omc_logger_flags, params_info_list,
        percentage, pos)
    temp_str = temp_str + this_param_str

    perturbate_param_and_run_str = temp_str
    return perturbate_param_and_run_str


def strForParamPerturbationForParamInPosition(csv_file_name_modelica_function, include_param_val_rollback, model_name,
                                              omc_logger_flags, params_info_list, percentage, pos):
    param_default, param_name, param_new_value = paramInfoForPos(params_info_list, percentage, pos)
    # Include the roll back of the param val to default because this is not the last param
    this_param_str = strForParamPerturbationFromParamInfo(
        csv_file_name_modelica_function, model_name, omc_logger_flags, param_default, param_name, param_new_value,
        include_param_val_rollback)
    # Join all the strs into one
    return this_param_str


def paramInfoForPos(params_info_list, percentage, pos):
    param_info_dict = params_info_list[pos]
    param_name = param_info_dict["name"]
    param_default = param_info_dict["initial_val"]
    # Calculate param new value from initial value and percentage
    param_new_value = param_default * (1 + percentage / 100)
    return param_default, param_name, param_new_value


def strForParamPerturbationFromParamInfo(csv_file_name_modelica_function, model_name, omc_logger_flags, param_default,
                                         param_name,
                                         param_new_value, include_param_val_rollback):
    # Human readable comment in resulting .mos
    comment_tag_str = "// Perturbing parameter: {param_name}".format(param_name=param_name)
    # Simulation file name
    filename_and_cmd_defs_str = strForFilenameAndCmdDefs(csv_file_name_modelica_function, param_name, model_name,
                                                         omc_logger_flags)
    # Set parameter with new value, run, return parameter to default value
    set_new_value_str = set_xml_value_skeleton.format(model_name=model_name, param_name=param_name,
                                                      param_val=param_new_value)
    run_cmd_str = run_system_command_str
    set_default_value_back_str = set_xml_value_skeleton.format(model_name=model_name, param_name=param_name,
                                                               param_val=param_default)
    # Join the "perturb, run, de-perturb" strs into one
    base_strs_to_include = [comment_tag_str, filename_and_cmd_defs_str, set_new_value_str, run_cmd_str]
    # See if we have to include or not the xml init rollback
    if include_param_val_rollback:
        strs_to_include = base_strs_to_include + [set_default_value_back_str]
    else:
        strs_to_include = base_strs_to_include
    this_param_str = "\n".join(strs_to_include)
    return this_param_str


def strForLoadingAndBuilding(mo_file, model_name, startTime, stopTime):
    load_and_build_str = load_and_build_skeleton.format(mo_file=mo_file, model_name=model_name, startTime=startTime,
                                                        stopTime=stopTime)
    return load_and_build_str


def strForFilenameAndCmdDefs(csv_file_name_modelica_function, param_name, model_name, omc_logger_flags):
    file_name_str = "file_name_i := " + '"' + csv_file_name_modelica_function(param_name) + '";'
    # cmd str
    cmd_str = ""
    if platform.system() == "Linux":
        cmd_str = linux_cmd_skeleton.format(model_name=model_name, omc_logger_flags=omc_logger_flags)
    elif platform.system() == "Windows":
        cmd_str = windows_cmd_skeleton.format(model_name=model_name, omc_logger_flags=omc_logger_flags)
    else:
        logger.error(
            "This script was tested only on Windows and Linux. The way to execute for another platform has not been set")
    filename_and_cmd_defs_str = "\n  " + file_name_str + cmd_str
    return filename_and_cmd_defs_str


load_and_build_skeleton = \
    """// load the file
print("Loading Modelica\\n");
loadModel(Modelica); //new OMC version stopped importing Modelica model
print("Loading file:{mo_file}\\n");
loadFile("{mo_file}"); getErrorString();
// build the model once
print("Building model:{model_name}\\n");
buildModel({model_name}, startTime={startTime},stopTime={stopTime},outputFormat="csv",stepSize=1); getErrorString();"""
# CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
windows_cmd_skeleton = \
    """
  cmd := "{model_name}.exe {omc_logger_flags} "+ "-r="+file_name_i + " -noEventEmit";"""
# CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
linux_cmd_skeleton = \
    """
  cmd := "./{model_name} {omc_logger_flags} "+ "-r="+file_name_i + " -noEventEmit";"""
# CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
set_xml_value_skeleton = \
    """  setInitXmlStartValue("{model_name}_init.xml", "{param_name}", String({param_val}) , "{model_name}_init.xml");"""
run_system_command_str = \
    """  print("Running command: "+cmd+"\\n");
  system(cmd);
  getErrorString();"""
