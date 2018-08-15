# Mine
import filesystem.files_aux as files_aux
class ModelicaModelBuilder():
    mos_script_skeleton =\
    (
        """print("Loading Modelica");\n"""
        """loadModel(Modelica);\n"""
    )
    def __init__(self):
        pass
    def writeMOSScriptToPath(self,file_path):
        files_aux.writeStrToFile(self.mos_script_skeleton,file_path)

