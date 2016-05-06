import platform

#Posibles lv para el omc_logger:
# LOG_DEBUG: muestra todos los valores leidos del .xml (3k lineas)
# LOG_SOLVER: muestra informacion sobre la jacobiana
# omc_logger_flags = "-w -lv=LOG_SOLVER"
# omc_logger_flags = "-w"
omc_logger_flags = ""
def main():
    pass
def createMos(mo_file,model_name,sweep_vars,iterations,output_mos_path,startTime,stopTime,fixed_params,sweep_value_formula_str,csv_file_name_modelica):
    load_and_build_str = strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime)
    fixed_params_str = strForFixedParams(fixed_params,model_name)
    for_declaration_str = strForForDeclaration(iterations)
    sweep_value_str = strForSweepValue(iterations,sweep_value_formula_str)
    sweeping_vars_str = strForSweepingVars(model_name,sweep_vars)
    full_system_call_str =  strForFullSystemCall(model_name,csv_file_name_modelica,omc_logger_flags)
    end_for_str = strForEndFor()
    final_str = load_and_build_str + fixed_params_str + for_declaration_str + \
                sweep_value_str    + sweeping_vars_str + full_system_call_str + \
                end_for_str
    writeStrToFile(final_str,output_mos_path)


def strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime):
    load_and_build_str = load_and_build_skeleton.format(mo_file=mo_file,model_name=model_name,startTime=startTime,stopTime=stopTime)
    return load_and_build_str

def strForFixedParams(fixed_params,model_name):
    fixed_params_str =""
    for var,value in fixed_params:
        set_param_str = fixed_params_skeleton.format(model_name=model_name,var_name=var,value=value)
        fixed_params_str = fixed_params_str + set_param_str
    return fixed_params_str

def strForForDeclaration(iterations):
    for_declaration_str = for_declaration_skeleton.format(iterations=iterations)
    return for_declaration_str

def strForSweepValue(iterations,sweep_value_formula_str):
    sweep_value_str = "\n  value := "+ sweep_value_formula_str + ";"
    return sweep_value_str

def strForSweepingVars(model_name,sweep_vars):
    sweeping_vars_str = ""
    for var in sweep_vars:
        var_sweep_str = sweeping_vars_skeleton.format(model_name=model_name,sweep_var=var)
        sweeping_vars_str = sweeping_vars_str + var_sweep_str
    return sweeping_vars_str
def strForFullSystemCall(model_name,csv_file_name_modelica,omc_logger_flags):
    file_name_str = "file_name_i := " + csv_file_name_modelica
    #cmd str
    cmd_str = ""
    if platform.system() == "Linux":
        cmd_str= linux_cmd_skeleton.format(model_name=model_name,omc_logger_flags=omc_logger_flags)
    elif platform.system() == "Windows":
        cmd_str= windows_cmd_skeleton.format(model_name=model_name,omc_logger_flags=omc_logger_flags)
    else:
        logger.error("This script was tested only on Windows and Linux. The way to execute for another platform has not been set")
    system_call_str = system_call_skeleton.format() #no parameters
    full_system_call_str = file_name_str + cmd_str + system_call_str

    return full_system_call_str

def strForEndFor():
    end_for_str = "\n end for;"
    return end_for_str
def writeStrToFile(str_,file_path):
    with open(file_path, 'w') as outputFile:
        outputFile.write(str_)
    return 0


#String skeletons: (the names inside "{ }" are variables)
load_and_build_skeleton= \
"""// load the file
print("Loading file:{mo_file}\\n");
loadFile("{mo_file}");
getErrorString();
// build the model once
//buildModel({model_name});
print("Building model:{model_name}\\n");
buildModel({model_name}, startTime={startTime},stopTime={stopTime},outputFormat="csv");
getErrorString();"""
fixed_params_skeleton= \
"""
setInitXmlStartValue("{model_name}_init.xml", "{var_name}", String({value}) , "{model_name}_init.xml");
getErrorString();"""
#CAREFUL! run_and_plot_model.py assumes that i goes from 0 to (iterations-1)
for_declaration_skeleton=\
"""
for i in 0:({iterations}-1) loop"""
sweeping_vars_skeleton= \
"""
  setInitXmlStartValue("{model_name}_init.xml", "{sweep_var}", String(value) , "{model_name}_init.xml");
  getErrorString();
"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
file_name_skeleton= \
"""
  file_name_i := "{model_name}_" + String(i) + "_res.csv";"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
windows_cmd_skeleton= \
"""
  cmd := "{model_name}.exe {omc_logger_flags} "+ "-r="+file_name_i;"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
linux_cmd_skeleton= \
"""
  cmd := "./{model_name} {omc_logger_flags} "+ "-r="+file_name_i;"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
system_call_skeleton= \
"""
  print("Running command: "+cmd+"\\n");
  system(cmd);
  getErrorString();
  //plot(plot_var,fileName=file_name_i,externalWindow=true);"""#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)



if __name__ == "__main__":
    main()
