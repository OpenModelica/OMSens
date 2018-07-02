#Imports:
# Base:
import sys
import argparse
from xml.dom import minidom
import logging
logger = logging.getLogger("-- S&R XML file --") #un logger especifico para este modulo
#Globals:
script_description ="""Search & Replace parameters values in an XML file"""
def main():
    logging.basicConfig(level=logging.INFO) #to show on stdout and only info
    xml_origin_path, xml_new_path ,stopTime,params_list,values_list = setUpScript()
    return replaceParametersValues(xml_origin_path, xml_new_path, stopTime, params_list,values_list)


def setUpScript():
    parser = argparse.ArgumentParser(description=script_description,prefix_chars='@')   # "@" instead of "-" because the scripts break if with"-" and it receives neg numbers
    parser.add_argument('@@fromFile', dest="fromFile", action='store_true')
    parser.add_argument('@@xml_origin_path', help='The path to the xml to be read',type=str)
    parser.add_argument('@@xml_new_path', help='The path to the new xml to be created',type=str)
    parser.add_argument('@@stopTime', help='The desired stopTime (the startTime is fixed for now)',type=int)
    parser.add_argument('@@pl', nargs='+', help='The list of parameters to modify', type=str)
    parser.add_argument('@@vl', nargs='+', help='The list of new values to set', type=float)
    args = parser.parse_args()
    if args.fromFile:
        # If the "@@fromFile" flag is set, we have to read from file instead of from the arguments in the command line
        # (useful when there are a lot of parameters to set)
        # IMPORTANT: for now the input file is fixed as "inputSandR.txt"
        # Order: xml_origin_path, xml_new_path, stopTime, params_list, values_list.
        scriptInput_path = "inputSandR.txt"
        script_inputs = readStrFromFile(scriptInput_path)
        # Separate file into newlines
        script_inputs_lines = script_inputs.splitlines()
        # First, xml_origin_path (string)
        xml_origin_path = script_inputs_lines[0].replace(" ","")
        # Then,  xml_new_path (string)
        xml_new_path = script_inputs_lines[1].replace(" ","")
        # Then,  stopTime (int)
        stopTime = int(script_inputs_lines[2])
        # Then, params_list (list of strings)
        params_list = script_inputs_lines[3].split()
        # Then, values_list (list of floats)
        values_list_strs = script_inputs_lines[4].split()
        values_list = [float(x) for x in values_list_strs]
    else:
        # Get the arguments from the command line args
        xml_origin_path = args.xml_origin_path
        xml_new_path = args.xml_new_path
        stopTime = args.stopTime
        params_list = args.pl
        values_list = args.vl
    return xml_origin_path, xml_new_path, stopTime, params_list,values_list

def replaceParametersValues(xml_origin_path, xml_new_path ,stopTime,params_list,values_list):
    # Parse xml using minidom
    try:
        xmldoc = minidom.parse(xml_origin_path)
    except FileNotFoundError:
        # IF the file doesn't exist, raise error
        logger.error("ERROR: XML NOT FOUND! Run from root of modelicascripts project and not inside this folder so the path to read the .xml makes sense to the script")
        sys.exit(1)
    # Set the stopTime
    # (it assumes that there is only one "DefaultExperiment" node)
    defaultExperiment_node = xmldoc.getElementsByTagName('DefaultExperiment')[0]
    defaultExperiment_node.setAttribute("stopTime",str(stopTime))
    # Set the parameters
    # Get the ScalarVariables nodes
    scalarVariable_nodes_list = xmldoc.getElementsByTagName('ScalarVariable')
    # Get the "root" parameters (the parameters of the main model, not from submodels)
    root_parameters_nodes = [x for x in scalarVariable_nodes_list if "." not in x.getAttribute("name") and x.getAttribute("variability")=="parameter"] #doesn't contain a dot and is of variability parameter
    # Put the params names and values into a dict for easier reference and removal
    params_dict = dict(zip(params_list,values_list))
    # Iterate the root parameters (the parameters from the main model and not from one of the submodels)
    for param_node in root_parameters_nodes:
        param_name = param_node.getAttribute("name")
        if param_name in params_dict:
            param_value = params_dict[param_name]
            # Get its "<Real ..>" subnode
            real_sub_node = param_node.getElementsByTagName('Real')[0]
            # Modify the start value
            real_sub_node.setAttribute("start",str(param_value))
            # Remove the parameter from the params_dict dict
            del params_dict[param_name]
    # After iterating the standard params, the set should be empty. IF not, raise an error and exit
    if len(params_dict) > 0:
        logger.error("ERROR: The following list contains invalid parameters:" + str(params_dict.keys()))
        sys.exit(1)
    # No errors have been raised, so write to the specified path the modified .xml
    with open(xml_new_path,"w") as outputFile:
        xmldoc.writexml(outputFile)
    return 0

def readStrFromFile(file_path):
    with open(file_path, 'r') as myfile:
        data = myfile.read()
    return data

if __name__ == "__main__":
    main()
