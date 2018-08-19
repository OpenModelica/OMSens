# Std
import os
import xml.etree.ElementTree as XMLTree

class CompiledModelicaModel():
    def __init__(self,model_name, binary_file_path):
        # Attrs from args
        self.model_name = model_name
        self.binary_file_path = binary_file_path
        # Other attrs
        xml_file_path = xmlFilePathForModel(self.binary_file_path, self.model_name)
        self.xml_file_path = xml_file_path
        # Read XML from XML file
        xml_tree = XMLTree.parse(self.xml_file_path)
        self.xml_tree = xml_tree

    def setParameterStartValue(self,param_name,param_val):
        # Get XML root
        root = self.xml_tree.getroot()
        # Find element with vars and parameters
        modelvars_element = [ e for e in root.getchildren() if e.attrib =="ModelVariables"][0]
        # Find parameter
        param_element = [x for x in modelvars_element.getchildren() if
                         x.tag == "ScalarVariable" and x.attrib["name"] == param_name][0]
        # Get value element for param
        param_value_element = param_element.getchildren()[0]
        # Change value
        param_value_element.attrib["start"] = param_val
        # Write XML to disk
        self.xml_tree.write(self.xml_file_path)

# Auxs
def xmlFilePathForModel(binary_file_path, model_name):
    binary_folder_path = os.path.dirname(binary_file_path)
    xml_file_name = "{0}_init.xml".format(model_name)
    xml_file_path = os.path.join(binary_folder_path, xml_file_name)
    return xml_file_path
