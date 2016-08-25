#Std
import platform
#Mine
import filesystem.files_aux

#Posibles lv para el omc_logger:
# LOG_DEBUG: muestra todos los valores leidos del .xml (3k lineas)
# LOG_SOLVER: muestra informacion sobre la jacobiana
# omc_logger_flags = "-w -lv=LOG_SOLVER"
# omc_logger_flags = "-w"
omc_logger_flags = ""
def main():
    createMos_kwargs = {
       "mo_file": "MO_FILE.mo",
       "model_name": "MODEL_NAME_GUACHO",
       "parameters_to_perturbate_tuples" : [("param1",1,2),("param2",3,4)],
       "output_mos_path" : "/tmp/asd.mos",
       "startTime": 1900,
       "stopTime": 1950,
       "csv_file_name_modelica_function": "{param_name}_perturbed.csv",
    }
    createMos(**createMos_kwargs)
    pass
def createMos(mo_file,model_name,parameters_to_perturbate_tuples,output_mos_path,startTime,stopTime,csv_file_name_modelica_function):
    load_and_build_str = strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime)
    perturbate_param_and_run_str = strForPerturbateParamAndRun(parameters_to_perturbate_tuples,model_name,csv_file_name_modelica_function,omc_logger_flags)

    final_str = load_and_build_str + perturbate_param_and_run_str
    filesystem.files_aux.writeStrToFile(final_str,output_mos_path)
    return 0

def strForPerturbateParamAndRun(parameters_to_perturbate_tuples,model_name,csv_file_name_modelica_function,omc_logger_flags):
    temp_str = ""
    for param_name,param_default,param_new_value in parameters_to_perturbate_tuples:
        comment_tag_str = "\n// Perturbing parameter: {param_name}".format(param_name=param_name)
        filename_and_cmd_defs_str =  strForFilenameAndCmdDefs(csv_file_name_modelica_function,param_name,model_name,omc_logger_flags)
        this_param_str=perturbate_param_and_run_skeleton.format(param_name=param_name, param_default=param_default, param_new_value=param_new_value, model_name=model_name)
        temp_str = temp_str + comment_tag_str + filename_and_cmd_defs_str + this_param_str
    perturbate_param_and_run_str = temp_str
    return perturbate_param_and_run_str
def strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime):
    load_and_build_str = load_and_build_skeleton.format(mo_file=mo_file,model_name=model_name,startTime=startTime,stopTime=stopTime)
    return load_and_build_str
def removeSpecialCharactersTo(param_name):
    wo_left_bracket  = param_name.replace("[","_bracket_")
    wo_both_brackets = wo_left_bracket.replace("]","_bracket")
    standarized_param_name = wo_both_brackets
    return standarized_param_name
def strForFilenameAndCmdDefs(csv_file_name_modelica_function,param_name,model_name,omc_logger_flags):
    standarized_param_name = removeSpecialCharactersTo(param_name)
    file_name_str = "file_name_i := " + '"'+csv_file_name_modelica_function(param_name)+'";'
    #cmd str
    cmd_str = ""
    if platform.system() == "Linux":
        cmd_str= linux_cmd_skeleton.format(model_name=model_name,omc_logger_flags=omc_logger_flags)
    elif platform.system() == "Windows":
        cmd_str= windows_cmd_skeleton.format(model_name=model_name,omc_logger_flags=omc_logger_flags)
    else:
        logger.error("This script was tested only on Windows and Linux. The way to execute for another platform has not been set")
    filename_and_cmd_defs_str = "\n  " + file_name_str + cmd_str
    return filename_and_cmd_defs_str

load_and_build_skeleton= \
"""// load the file
print("Loading Modelica\\n");
loadModel(Modelica); //new OMC version stopped importing Modelica model
print("Loading file:{mo_file}\\n");
loadFile("{mo_file}"); getErrorString();
// build the model once
print("Building model:{model_name}\\n");
buildModel({model_name}, startTime={startTime},stopTime={stopTime},outputFormat="csv",stepSize=1); getErrorString();"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
windows_cmd_skeleton= \
"""
  cmd := "{model_name}.exe {omc_logger_flags} "+ "-r="+file_name_i;"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
linux_cmd_skeleton= \
"""
  cmd := "./{model_name} {omc_logger_flags} "+ "-r="+file_name_i;"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
perturbate_param_and_run_skeleton= \
"""
  setInitXmlStartValue("{model_name}_init.xml", "{param_name}", String({param_new_value}) , "{model_name}_init.xml");
  print("Running command: "+cmd+"\\n");
  system(cmd);
  getErrorString();
  setInitXmlStartValue("{model_name}_init.xml", "{param_name}", String({param_default}) , "{model_name}_init.xml");"""

if __name__ == "__main__":
    main()
