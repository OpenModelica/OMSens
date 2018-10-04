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
class UniparamSweepingMosWriter():
    def __init__(self,*args,**kwargs):
        pass
    def createMos(self,mo_file,model_name,sweep_vars,iterations,output_mos_path,startTime,stopTime,fixed_params,sweep_value_formula_str,csv_file_name_modelica):
        load_and_build_str        = strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime)
        check_if_valid_params_str = strForCheckingIfValidParams(model_name,sweep_vars,fixed_params)
        fixed_params_str          = strForFixedParams(fixed_params,model_name)
        for_declaration_str       = "\n"   + strForForDeclaration(iterations)
        sweep_value_str           = "\n  " + strForSweepValue(iterations,sweep_value_formula_str)
        sweeping_params_str       = strForSweepingParamsWithSameValue(model_name,sweep_vars)
        full_system_call_str      = strForFullSystemCall(model_name,csv_file_name_modelica,omc_logger_flags)
        end_for_str               = strForEndFor()
        final_str                 = load_and_build_str + fixed_params_str + for_declaration_str + \
                    sweep_value_str    + sweeping_params_str + full_system_call_str + \
                    end_for_str
        filesystem.files_aux.writeStrToFile(final_str,output_mos_path)
        return 0

class MultiparamSweepingMosWriter():
    def __init__(self,*args,**kwargs):
        pass
    # def createMos(self,mo_file,model_name,sweep_vars,iterations,output_mos_path,startTime,stopTime,fixed_params,sweep_value_formula_str,csv_file_name_modelica):
    def createMos(self, model_name, startTime, stopTime, mo_file, sweep_params_settings_list, fixed_params,output_mos_path,csv_file_name_modelica_skeleton,mos_copy_path=False):
        # Initial settings of the .mos script
        load_and_build_str   = strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime)
        fixed_params_str     = strForFixedParams(fixed_params,model_name)

        # A "for loop" for each parameter to sweep
        params_str_list = []
        param_padding = ""   # white spaces to add for each nested "for loop" (so they are tabularized and easier to read)
        i_total_init_str = "i_total := 0;"
        end_for_list = []
        for param_settings in sweep_params_settings_list:
            param_name_wo_SpChars  = removeSpecialCharactersTo(param_settings.param_name)
            i_param                = "i_"+param_name_wo_SpChars
            value_var_name         = "value_"+param_name_wo_SpChars                       # "value_pop_init :        = ..."
            formula_instantiated   = param_settings.formula(i_param)
            csv_file_name_modelica = csv_file_name_modelica_skeleton.format(i_name="i_total")

            for_declaration_str    = param_padding + strForForDeclaration(param_settings.iterations,i_param)
            end_for_list.insert(0,param_padding + "end for;")  # we accumulate the "end for;" inversely from the param order and include it after the system call and i_total_succ_str
            param_padding          = param_padding + "  "   # white spaces to add for each nested "for loop" (so they are tabularized and easier to read)
            sweep_value_str        = param_padding + strForSweepValue(param_settings.iterations,formula_instantiated,value_var_name)
            set_param_val_str      = param_padding + set_param_val_skeleton.format(model_name= model_name,sweep_param = param_settings.param_name,value_var_name = value_var_name)
            this_param_str         = "\n".join([for_declaration_str,sweep_value_str,set_param_val_str])
            params_str_list.append(this_param_str)
            full_system_call_str   = strForFullSystemCall(model_name,csv_file_name_modelica,omc_logger_flags,param_padding)
            i_total_succ_str       = param_padding +"i_total := i_total + 1;"
        params_str_w_newl  = "\n".join(params_str_list)
        end_for_str_w_newl = "\n".join(end_for_list)

        final_str          = "\n".join([load_and_build_str, fixed_params_str, i_total_init_str,
                                        params_str_w_newl, full_system_call_str, i_total_succ_str,
                                        end_for_str_w_newl])
        filesystem.files_aux.writeStrToFile(final_str,output_mos_path)
        if mos_copy_path:
            # If a copy of the mos file needs to be written
            filesystem.files_aux.writeStrToFile(final_str,mos_copy_path)
        return 0

def removeSpecialCharactersTo(param_name):
    wo_left_bracket  = param_name.replace("[","_bracket_")
    wo_both_brackets = wo_left_bracket.replace("]","_bracket")
    standarized_param_name = wo_both_brackets
    return standarized_param_name

def strForCheckingIfValidParams(model_name,sweep_vars,fixed_params):
    fixed_params_names =[param_tuple[0] for param_tuple in fixed_params]
    all_params = sweep_vars+fixed_params_names
    params_list_str = paramsListInModelicaFormat(all_params)
    check_if_valid_params_str = check_if_valid_params_skeleton.format(model_name=model_name,params_list=params_list_str)
    return check_if_valid_params_str
def paramsListInModelicaFormat(all_params):
    params_list = "{"+",".join(['"'+param+'"' for param in all_params])+"}"
    return params_list
def strForLoadingAndBuilding(mo_file,model_name,startTime,stopTime):
    load_and_build_str = load_and_build_skeleton.format(mo_file=mo_file,model_name=model_name,startTime=startTime,stopTime=stopTime)
    return load_and_build_str

def strForFixedParams(fixed_params,model_name):
    fixed_params_str =""
    for var,value in fixed_params:
        set_param_str = fixed_params_skeleton.format(model_name=model_name,var_name=var,value=value)
        fixed_params_str = fixed_params_str + set_param_str
    return fixed_params_str

def strForForDeclaration(iterations,i_name="i"):
#CAREFUL! run_and_plot_model.py assumes that i goes from 0 to (iterations-1)
    for_declaration_str = "for {i_name} in 0:({iterations}-1) loop".format(iterations=iterations,i_name=i_name)
    return for_declaration_str

def strForSweepValue(iterations,sweep_value_formula_str,value_var_name="value"):
    sweep_value_str = "{value_var_name} := ".format(value_var_name=value_var_name) + sweep_value_formula_str + ";"
    return sweep_value_str

def strForSweepingParamsWithSameValue(model_name,sweep_vars,value_var_name="value"):
    sweeping_params_str = ""
    for var in sweep_vars: # Take into account that these vars (params) will all be set the same value!
        var_sweep_str = "\n  " + set_param_val_skeleton.format(model_name=model_name,sweep_param=var,value_var_name=value_var_name)
        sweeping_params_str = sweeping_params_str + var_sweep_str
    return sweeping_params_str
def strForFullSystemCall(model_name,csv_file_name_modelica,omc_logger_flags,param_padding=""):
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
    full_system_call_str = param_padding + file_name_str        + "\n" + \
                           param_padding + cmd_str              + "\n" + \
                           param_padding + system_call_str
    return full_system_call_str

def strForEndFor():
    end_for_str = "\n end for;"
    return end_for_str


#String skeletons: (the names inside "{ }" are variables)
load_and_build_skeleton= \
"""// load the file
print("Loading file:{mo_file}\\n");
loadModel(Modelica); //new OMC version stopped importing Modelica model
loadFile("{mo_file}");
getErrorString();
// build the model once
//buildModel({model_name});
print("Building model:{model_name}\\n");
buildModel({model_name}, startTime={startTime},stopTime={stopTime},outputFormat="csv",stepSize=1);
getErrorString();"""
fixed_params_skeleton= \
"""
setInitXmlStartValue("{model_name}_init.xml", "{var_name}", String({value}) , "{model_name}_init.xml");
getErrorString();"""
set_param_val_skeleton= \
"""setInitXmlStartValue("{model_name}_init.xml", "{sweep_param}", String({value_var_name}) , "{model_name}_init.xml");getErrorString();"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
windows_cmd_skeleton= \
"""cmd := "{model_name}.exe {omc_logger_flags} "+ "-r="+file_name_i;"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
linux_cmd_skeleton= \
"""cmd := "./{model_name} {omc_logger_flags} "+ "-r="+file_name_i;"""
#CAREFUL! Don't change file_name_i. May break everything (we assume in run_and_plot_model.py that the file_names will follow this standard)
system_call_skeleton= \
"""print("Running command: "+cmd+"\\n"); system(cmd); getErrorString();"""
check_if_valid_params_skeleton= \
""" params := getParameterNames({model_name});
my_params := {params_list};
all_params_are_valid:= true;
for my_param in my_params loop
  my_param_is_valid := false;
  for available_param in params loop
      my_param_is_valid:= my_param_is_valid or my_param==available_param;
  end for;
  all_params_are_valid := all_params_are_valid and my_param_is_valid;
end for;
print(String(all_params_are_valid));"""

if __name__ == "__main__":
    main()
