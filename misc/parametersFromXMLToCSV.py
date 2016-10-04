# This script:
# 1) Reads the .XML for a World3 build
# 2) Gets the root parameters
# 3) For all of the root parameters, it prints its name and its value as csv
from xml.dom import minidom
import sys
try:
    xmldoc = minidom.parse('resource/standard_run.xml')
except FileNotFoundError:
    print("ERROR: XML NOT FOUND! Run from root of modelicascripts project and not inside this folder so the path to read the .xml makes sense to the script")
    sys.exit(1)
itemlist = xmldoc.getElementsByTagName('ScalarVariable')
root_parameters_nodes = [x for x in itemlist if "." not in x.getAttribute("name") and x.getAttribute("variability")=="parameter"] #doesn't contain a dot and is of variability parameter
print("Parameter name, value")
for param_node in root_parameters_nodes:
    param_name = param_node.getAttribute("name")
    real_sub_node = param_node.getElementsByTagName('Real')[0]
    param_val = real_sub_node.getAttribute("start")
    print(param_name+","+param_val)


