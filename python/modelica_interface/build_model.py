# Mine
import filesystem.files_aux as files_aux
class ModelicaModelBuilder():
    mos_script_skeleton =\
    (
        """print("Loading Modelica");\n"""
        """loadModel(Modelica);getErrorString();\n"""
        """print("Loading model in path {model_file_path}");\n"""
        """loadFile("{model_file_path}"); getErrorString();\n"""
        """print("Building model {model_name}");\n"""
        """buildModel({model_name}, startTime={startTime},stopTime={stopTime},outputFormat="csv"); getErrorString();"""
    )

    def __init__(self, model_name, start_time, stop_time, model_file_path):
        self.model_name      = model_name
        self.start_time       = start_time
        self.stop_time        = stop_time
        self.model_file_path = model_file_path

    def mosScriptString(self):
        mos_script_str = self.mos_script_skeleton.format(model_file_path= self.model_file_path,
                                                         model_name     = self.model_name,
                                                         startTime      = self.start_time,
                                                         stopTime       = self.stop_time)
        return mos_script_str

    def writeMOSScriptToPath(self,file_path):
        mos_script_str = self.mosScriptString()
        files_aux.writeStrToFile(mos_script_str,file_path)

