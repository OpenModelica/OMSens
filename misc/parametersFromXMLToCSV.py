# This script:
# 1) Reads the .XML for a World3 build
# 2) Gets the root parameters
# 3) For all of the root parameters, it prints its name and its value as csv
from xml.dom import minidom
xmldoc = minidom.parse('resource/standard_run.xml')
itemlist = xmldoc.getElementsByTagName('ScalarVariable')
root_parameters_nodes = [x for x in itemlist if "." not in x.getAttribute("name") and x.getAttribute("variability")=="parameter"] #doesn't contain a dot and is of variability parameter
print("Parameter name, value")
for param_node in root_parameters_nodes:
    param_name = param_node.getAttribute("name")
    real_sub_node = param_node.getElementsByTagName('Real')[0]
    param_val = real_sub_node.getAttribute("start")
    print(param_name+","+param_val)


