# This script:
# 1) Reads the .XML for a World3 build
# 2) Gets the root parameters
# 3) For all of the root parameters, it prints its name and its value as csv
# Std
from xml.dom import minidom
import sys
# Mine
import filesystem.files_aux

# GLOBAL
output_path = "tmp/vars_and_params_csv_defaults_table.csv"

try:
    xmldoc = minidom.parse('resource/standard_run.xml')
except FileNotFoundError:
    print("ERROR: XML NOT FOUND! Run from root of modelicascripts project and not inside this folder so the path to read the .xml makes sense to the script")
    sys.exit(1)
itemlist = xmldoc.getElementsByTagName('ScalarVariable')
root_parameters_nodes = [x for x in itemlist if "." not in x.getAttribute("name") and x.getAttribute("variability")=="parameter"] #doesn't contain a dot and is of variability parameter
accum_csv_str = "name,description,variability,default_value(if_any)"
for var_node in itemlist:
    var_name = var_node.getAttribute("name")
    var_description = '"'+var_node.getAttribute("description")+'"'
    var_variability = var_node.getAttribute("variability") #change continuos to "variable" if its a variable and not a parameter
    if var_variability == "continuous":
        # If in the xml the var variability is set to continuous then that means that it's a variable
        var_variability = "variable"
        var_default = "-"
    else:
        try:
            real_sub_node = var_node.getElementsByTagName('Real')[0]
            var_default = real_sub_node.getAttribute("start")
        except IndexError:
            var_default = "None"
    str_line = ",".join([var_name,var_description,var_variability,var_default])
    accum_csv_str = accum_csv_str +"\n"+ str_line
    print(str_line)
filesystem.files_aux.writeStrToFile(accum_csv_str,output_path)

# # Root parameters:
# print("Parameter name, value")
# for param_node in root_parameters_nodes:
#     param_name = param_node.getAttribute("name")
#     real_sub_node = param_node.getElementsByTagName('Real')[0]
#     param_val = real_sub_node.getAttribute("start")
#     param_desc = param_node.getAttribute("description")
#     print(param_name+","+param_val+","+param_desc)
