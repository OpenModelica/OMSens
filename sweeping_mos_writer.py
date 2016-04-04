#Posibles lv para el omc_logger:
# LOG_DEBUG: muestra todos los valores leidos del .xml (3k lineas)
# LOG_SOLVER: muestra informacion sobre la jacobiana
# omc_logger_flags = "-w -lv=LOG_SOLVER"
# omc_logger_flags = "-w"
omc_logger_flags = ""
def main():
    pass
def createMos(mo_file,model_name,sweep_vars,plot_var,iterations,output_mos_path,startTime,stopTime,fixed_params,sweep_value_formula_str):
    load_and_build_str = strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime)
    fixed_params_str = strForFixedParams(fixed_params,model_name)
    for_declaration_str = strForForDeclaration(iterations)
    sweep_value_str = strForSweepValue(iterations,sweep_value_formula_str)
    sweeping_vars_str = strForSweepingVars(model_name,sweep_vars)
    system_call_str = strForSystemCall(model_name,omc_logger_flags)
    end_for_str = strForEndFor()
    final_str = load_and_build_str + fixed_params_str + for_declaration_str + \
                sweep_value_str    + sweeping_vars_str + system_call_str + \
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
def strForSystemCall(model_name,omc_logger_flags):
    system_call_str = system_call_skeleton.format(model_name=model_name,omc_logger_flags=omc_logger_flags)
    return system_call_str

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

for_declaration_skeleton=\
"""
for i in 0:({iterations}-1) loop"""
sweeping_vars_skeleton= \
"""
  setInitXmlStartValue("{model_name}_init.xml", "{sweep_var}", String(value) , "{model_name}_init.xml");
  getErrorString();
"""
system_call_skeleton= \
"""
  file_name_i := "{model_name}_" + String(i) + "_res.csv";
  cmd := "./{model_name} {omc_logger_flags} "+ "-r="+file_name_i;
  print("Running command: "+cmd+"\\n");
  system(cmd);
  getErrorString();
  //plot(plot_var,fileName=file_name_i,externalWindow=true);"""



if __name__ == "__main__":
    main()
