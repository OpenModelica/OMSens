# Mine
import filesystem.files_aux as files_aux
class ModelicaModelBuilder():
    mos_script_skeleton =\
    (
        """print("Loading Modelica");\n"""
        """loadModel(Modelica);getErrorString();\n"""
        """print("Loading model in path {model_file_path}");\n"""
        """loadFile("{model_file_path}"); getErrorString();\n"""
    )
    def __init__(self, model_file_path):
        self.model_file_path = model_file_path

    def mosScriptString(self):
        mos_script_str = self.mos_script_skeleton.format(model_file_path=self.model_file_path)
        return mos_script_str

    def writeMOSScriptToPath(self,file_path):
        mos_script_str = self.mosScriptString()
        files_aux.writeStrToFile(mos_script_str,file_path)

