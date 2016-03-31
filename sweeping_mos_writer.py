#Posibles lv para el omc_logger:
# LOG_DEBUG: muestra todos los valores leidos del .xml (3k lineas)
# LOG_SOLVER: muestra informacion sobre la jacobiana
# omc_logger_flags = "-w -lv=LOG_SOLVER"
# omc_logger_flags = "-w"
omc_logger_flags = ""
def main():
    pass
def createMos(mo_file,model_name,sweep_vars,plot_var,initial,increment,iterations,output_mos_path,startTime,stopTime,fixed_params):
    load_and_build_str = load_and_build_skeleton.format(mo_file=mo_file,model_name=model_name,startTime=startTime,stopTime=stopTime)
    fixed_params_str =""
    for var,value in fixed_params:
        set_param_str = fixed_params_skeleton.format(model_name=model_name,var_name=var,value=value)
        fixed_params_str = fixed_params_str + set_param_str
    for_declaration_str = for_declaration_skeleton.format(initial=initial,increment=increment,iterations=iterations)
    sweeping_vars_str = ""
    for var in sweep_vars:
        var_sweep_str = sweeping_vars_skeleton.format(model_name=model_name,sweep_var=var)
        sweeping_vars_str = sweeping_vars_str + var_sweep_str
    ending_str = call_and_endfor_skeleton.format(model_name=model_name,omc_logger_flags=omc_logger_flags)
    final_str = load_and_build_str + fixed_params_str + for_declaration_str + sweeping_vars_str + ending_str
    writeStrToFile(final_str,output_mos_path)



def writeStrToFile(str_,file_path):
    with open(file_path, 'w') as outputFile:
        outputFile.write(str_)
    return 0


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
for i in 0:({iterations}-1) loop
  value := {initial} + i*{increment};"""
sweeping_vars_skeleton= \
"""
  setInitXmlStartValue("{model_name}_init.xml", "{sweep_var}", String(value) , "{model_name}_init.xml");
  getErrorString();
"""
call_and_endfor_skeleton= \
"""
  file_name_i := "{model_name}_" + String(i) + "_res.csv";
  cmd := "./{model_name} {omc_logger_flags} "+ "-r="+file_name_i;
  print("Running command: "+cmd+"\\n");
  system(cmd);
  getErrorString();
  //plot(plot_var,fileName=file_name_i,externalWindow=true);
end for;
"""



if __name__ == "__main__":
    main()
