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
       "csv_file_name_modelica_skeleton": "{param_name}_perturbated.csv",
    }
    createMos(**createMos_kwargs)
    pass
def createMos(mo_file,model_name,parameters_to_perturbate_tuples,output_mos_path,startTime,stopTime,csv_file_name_modelica_skeleton):
    load_and_build_str = strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime)
    ### cambiar un parámetro, correr, y volver a su default
    perturbate_param_and_run_str = strForPerturbateParamAndRun(parameters_to_perturbate_tuples,model_name,csv_file_name_modelica_skeleton,omc_logger_flags)

    # cambiar el finaL_str
    final_str = load_and_build_str + perturbate_param_and_run_str
    filesystem.files_aux.writeStrToFile(final_str,output_mos_path)
    return 0

    ### cambiar un parámetro, correr, y volver a su default
def strForPerturbateParamAndRun(parameters_to_perturbate_tuples,model_name,csv_file_name_modelica_skeleton,omc_logger_flags):
    temp_str = ""
    for param_name,param_default,param_new_value in parameters_to_perturbate_tuples:
        comment_tag_str = "\n// Perturbing parameter: {param_name}".format(param_name=param_name)
        filename_and_cmd_defs_str =  strForFilenameAndCmdDefs(csv_file_name_modelica_skeleton,param_name,model_name,omc_logger_flags)
        this_param_str=perturbate_param_and_run_skeleton.format(param_name=param_name, param_default=param_default, param_new_value=param_new_value, model_name=model_name)
        temp_str = temp_str + comment_tag_str + filename_and_cmd_defs_str + this_param_str
    perturbate_param_and_run_str = temp_str
    return perturbate_param_and_run_str
def strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime):
    load_and_build_str = load_and_build_skeleton.format(mo_file=mo_file,model_name=model_name,startTime=startTime,stopTime=stopTime)
    return load_and_build_str
def removeSpecialCharactersTo(param_name):
    wo_left_bracket  = param_name.replace("[","bracket")
    wo_both_brackets = wo_left_bracket.replace("]","bracket")
    standarized_param_name = wo_both_brackets
    return standarized_param_name
def strForFilenameAndCmdDefs(csv_file_name_modelica_skeleton,param_name,model_name,omc_logger_flags):
    standarized_param_name = removeSpecialCharactersTo(param_name)
    file_name_str = "file_name_i := " + csv_file_name_modelica_skeleton.format(param_name=standarized_param_name)
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

#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
file_name_skeleton = \
"""
  file_name_i := {param_name}_perturbated.csv"""
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

####### BORRAR DE ACA PARA ABAJO:
# def createMos(mo_file,model_name,sweep_vars,iterations,output_mos_path,startTime,stopTime,fixed_params,sweep_value_formula_str,csv_file_name_modelica_skeleton):
#     load_and_build_str = strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime)
#     check_if_valid_params_str = strForCheckingIfValidParams(model_name,sweep_vars,fixed_params) #is not used yet because it needs work
#     fixed_params_str = strForFixedParams(fixed_params,model_name)
#     for_declaration_str = strForForDeclaration(iterations)
#     sweep_value_str = strForSweepValue(iterations,sweep_value_formula_str)
#     sweeping_vars_str = strForSweepingVars(model_name,sweep_vars)
#     full_system_call_str =  strForFullSystemCall(model_name,csv_file_name_modelica_skeleton,omc_logger_flags)
#     end_for_str = strForEndFor()
#     final_str = load_and_build_str + fixed_params_str + for_declaration_str + \
#                 sweep_value_str    + sweeping_vars_str + full_system_call_str + \
#                 end_for_str
#     filesystem.files_aux.writeStrToFile(final_str,output_mos_path)
#     return 0
#
#
# def strForCheckingIfValidParams(model_name,sweep_vars,fixed_params):
#     fixed_params_names =[param_tuple[0] for param_tuple in fixed_params]
#     all_params = sweep_vars+fixed_params_names
#     params_list_str = paramsListInModelicaFormat(all_params)
#     check_if_valid_params_str = check_if_valid_params_skeleton.format(model_name=model_name,params_list=params_list_str)
#     return check_if_valid_params_str
# def paramsListInModelicaFormat(all_params):
#     params_list = "{"+",".join(['"'+param+'"' for param in all_params])+"}"
#     return params_list
# def strForFixedParams(fixed_params,model_name):
#     fixed_params_str =""
#     for var,value in fixed_params:
#         set_param_str = fixed_params_skeleton.format(model_name=model_name,var_name=var,value=value)
#         fixed_params_str = fixed_params_str + set_param_str
#     return fixed_params_str
#
# def strForForDeclaration(iterations):
#     for_declaration_str = for_declaration_skeleton.format(iterations=iterations)
#     return for_declaration_str
#
# def strForSweepValue(iterations,sweep_value_formula_str):
#     sweep_value_str = "\n  value := "+ sweep_value_formula_str + ";"
#     return sweep_value_str
#
# def strForSweepingVars(model_name,sweep_vars):
#     sweeping_vars_str = ""
#     for var in sweep_vars:
#         var_sweep_str = sweeping_vars_skeleton.format(model_name=model_name,sweep_var=var)
#         sweeping_vars_str = sweeping_vars_str + var_sweep_str
#     return sweeping_vars_str
#
# def strForEndFor():
#     end_for_str = "\n end for;"
#     return end_for_str
#
#
# #String skeletons: (the names inside "{ }" are variables)
# fixed_params_skeleton= \
# """
# setInitXmlStartValue("{model_name}_init.xml", "{var_name}", String({value}) , "{model_name}_init.xml");
# getErrorString();"""
# #CAREFUL! run_and_plot_model.py assumes that i goes from 0 to (iterations-1)
# for_declaration_skeleton=\
# """
# for i in 0:({iterations}-1) loop"""
# sweeping_vars_skeleton= \
# """
#   setInitXmlStartValue("{model_name}_init.xml", "{sweep_var}", String(value) , "{model_name}_init.xml");
#   getErrorString();
# """
#
# check_if_valid_params_skeleton= \
# """ params := getParameterNames({model_name});
# my_params := {params_list};
# all_params_are_valid:= true;
# for my_param in my_params loop
#   my_param_is_valid := false;
#   for available_param in params loop
#       my_param_is_valid:= my_param_is_valid or my_param==available_param;
#   end for;
#   all_params_are_valid := all_params_are_valid and my_param_is_valid;
# end for;
# print(String(all_params_are_valid));"""
#
if __name__ == "__main__":
    main()
