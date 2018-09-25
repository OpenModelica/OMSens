# Std
import os
import re  # regex support
import shutil  # tempdir deletion
import tempfile  # tempdir creation
import unittest
import pandas

# Mine
import modelica_interface.build_model as build_model
import filesystem.files_aux as files_aux


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

    def test_builder_works_correctly_for_correct_inputs(self):
        # Write model to temp dir
        model_file_path = os.path.join(self._temp_dir,"model.mo")
        files_aux.writeStrToFile(model_str,model_file_path)
        # Test model params
        model_name = "Model"
        start_time = 1
        stop_time  = 2
        # Initialize and call model builder
        test_model_builder = build_model.ModelicaModelBuilder(model_name, start_time, stop_time, model_file_path)
        compiled_model = test_model_builder.buildToFolderPath(self._temp_dir)
        # Get script extensions regex
        regex = "{0}".format(model_name)
        # Get list of files from regex
        files_in_dir = os.listdir(self._temp_dir)
        files_for_regex = [x for x in files_in_dir if re.match(regex, x)]
        # Check that there is at least one file for regex
        if len(files_for_regex) < 1:
            error_msg = "The model builder should create at least one file in folder."
            self.fail(error_msg)
        # Test that the compiled model wrapper instance works correctly
        compiled_model.setParameterStartValue("a", 0)
        simulation_path = os.path.join(self._temp_dir, "simu.csv")
        simu_results = compiled_model.simulate(simulation_path)
        df_simu = pandas.read_csv(simulation_path)
        x_min = df_simu["x"].min()
        x_max = df_simu["x"].max()
        # We set the derivative slope as 0 so x should be a constant 1
        if not (x_min == x_max == 1):
            error_msg = "The parameter was not changed correctly"
            self.fail(error_msg)
        # Test that the default value for the params are backup-ed correctly
        param_def_val = compiled_model.defaultParameterValue("a")
        # We ask for the default value for a so it should be -1
        if not param_def_val == -1:
            error_msg = "The parameter default value was not backup-ed correctly"
            self.fail(error_msg)
        # Test that the current value for the params is returned correctly
        param_val = compiled_model.parameterValue("a")
        # We ask for the current value for a so it should be 0
        if not param_val == 0:
            error_msg = "The parameter current value was not returned correctly"
            self.fail(error_msg)
        # Test that the "quickSimulate" function returns the right value
        x_quick_simu = compiled_model.quickSimulate("x")
        if not (x_quick_simu == 1):
            error_msg = "The quick simulation didn't return the right value"
            self.fail(error_msg)
        # Test that the "set everything back to defaults" works
        compiled_model.restoreAllParametersToDefaultValues()
        param_val = compiled_model.parameterValue("a")
        if not param_val == -1:
            error_msg = "The parameter default value was not restored correctly"
            self.fail(error_msg)

# Auxs
model_str = \
"""class Model
  parameter Real a=-1;
  Real x(start=1,fixed=true);
equation
  der(x) = a*x;
end Model;"""
