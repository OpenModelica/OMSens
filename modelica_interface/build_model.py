# Std
import os
# Mine
import filesystem.files_aux as files_aux
import modelica_interface.run_omc as run_omc
from modelica_interface.compiled_model import CompiledModelicaModel


class ModelicaModelBuilder():
    mos_script_skeleton = \
    (
        # This shouldn't be the responsibility of the builder, but for now we leave it here
        """print("Loading Modelica");\n"""
        """loadModel(Modelica);getErrorString();\n"""
        """print("Loading model in path {model_file_path}");\n"""
        """loadFile("{model_file_path}"); getErrorString();\n"""
        """print("Building model {model_name}");\n"""
        """buildModel({model_name}, startTime={startTime},stopTime={stopTime},outputFormat="csv", numberOfIntervals={numberOfIntervals}); getErrorString();"""
    )

    def __init__(self, model_name, start_time, stop_time, model_file_path, number_of_intervals=300):
        # Attrs from args
        self.model_name        = model_name
        self.start_time        = start_time
        self.stop_time         = stop_time
        self.model_file_path   = model_file_path
        self.number_of_intervals = number_of_intervals
        # Hardcoded attrs
        self.mos_script_file_name = "builder.mos"

    def buildToFolderPath(self,dest_folder_path):
        # Write .mos script to folder
        mos_script_path = os.path.join(dest_folder_path, self.mos_script_file_name)
        self.writeMOSScriptToPath(mos_script_path)
        # Run mos script with OMC
        run_omc.runMosScript(mos_script_path)
        # Get binary path from folder and model name
        binary_file_path = os.path.join(dest_folder_path, self.model_name)
        # Initialize compiled model instance from path
        compiled_model = CompiledModelicaModel(self.model_name, binary_file_path)
        return compiled_model


    def mosScriptString(self):
        # There should be no backslashes (\) in paths, even in Windows
        file_path_wo_bslashes = self.model_file_path.replace("\\", "/")
        # This shouldn't be the responsibility of the builder, but for now we leave it here
        mos_script_str = self.mos_script_skeleton.format(model_file_path   = file_path_wo_bslashes,
                                                         model_name        = self.model_name,
                                                         startTime         = self.start_time,
                                                         numberOfIntervals = self.number_of_intervals,
                                                         stopTime          = self.stop_time)
        return mos_script_str

    def writeMOSScriptToPath(self,file_path):
        # This shouldn't be the responsibility of the builder, but for now we leave it here
        mos_script_str = self.mosScriptString()
        files_aux.writeStrToFile(mos_script_str,file_path)

