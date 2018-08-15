# Std
import os
import re  # regex support
import shutil  # tempdir deletion
import tempfile  # tempdir creation
import unittest

# Mine
import modelica_interface.build_model as build_model


class TestsBuildModel(unittest.TestCase):
    # setup y teardown de los tests
    def setUp(self):
        # Create tempdir and save its path
        self._temp_dir = tempfile.mkdtemp()
        self._temp_files = []  # each test case can create individual files

    def tearDown(self):
        pass
        shutil.rmtree(self._temp_dir)
        for f in self._temp_files:
            f.close()

    def test_builder_creates_files_in_folder(self):
        # Test model params
        model_name = "Model"
        start_time = 1
        stop_time  = 2

        # 1) Create mos that builds model
        # 1.1) Load Modelica library
        load_modelica_str = "loadModel(Modelica);"
        # 1.2) Load file for model
        load_model_file_skeleton = "loadFile({0}); getErrorString();"
        load_model_file_str = load_model_file_skeleton.format(model_name)
        # 1.3) Build model
        build_model_skeleton = """buildModel({0}, startTime={1},stopTime={2},outputFormat="csv"); getErrorString();"""
        build_model_str = build_model_skeleton.format(model_name,start_time,stop_time)
        # MOS Script string
        mos_script_parts = [load_modelica_str, load_model_file_str, build_model_str]
        mos_script_string = "\n".join(mos_script_parts)
        # ADAPTAR LO DE ARRIBA
        test_model_builder = build_model.ModelicaModelBuilder()
        mos_script_path = os.path.join(self._temp_dir,"mos_script.mos")
        test_model_builder.writeMOSScriptToPath(mos_script_path)
        # Get script extensions regex
        regex = '.*\.mos$'
        # Get list of files from regex
        files_in_dir = os.listdir(self._temp_dir)
        plot_files = [x for x in files_in_dir if re.match(regex, x)]
        # Check that there is at least one file for regex
        if len(plot_files) < 1:
            error_msg = "The model builder should create at least one file in folder."
            self.fail(error_msg)

# Auxs
model_str = \
"""loadString("
class Model
  parameter Real a=-1;
  Real x(start=1,fixed=true);
equation
  der(x) = a*x;
end Model;
");\n """
