# Std
import glob
import os
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
from io import StringIO
import numpy
import pathlib

# Mine
import modelica_interface.build_model as build_model
import filesystem.files_aux as files_aux
import vectorial.model_optimizer as model_optimizer_f


class TestIndividualSensitivityAnalysis(unittest.TestCase):
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
    # Tests:
    def test_one_param_min(self):
        # Get the base arguments for the 3 params example
        model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb, \
               lower_bounds, upper_bounds, max_or_min, epsilon, build_folder_path = \
            self.threeParamsModelOptimizerBaseArgsExample()
        # Replace the args so we only minimize one
        parameters_to_perturb = ["a"]
        lower_bounds = [-2]
        upper_bounds = [2]
        # Initialize optimizer
        model_optimizer = model_optimizer_f.ModelOptimizer(model_name, start_time, stop_time, model_file_path,
                                                           target_var_name, parameters_to_perturb, max_or_min,
                                                           build_folder_path)
        # Run optimizer
        x_opt_dict, f_opt = model_optimizer.optimize(lower_bounds, upper_bounds, epsilon)
        # Check that it optimized correctly the X
        correct_x_opt = -2
        x_opt = x_opt_dict["a"]
        if not numpy.isclose(correct_x_opt,x_opt,atol=epsilon):
            error_msg = "x_opt distance should be close to {0}" \
                        " but instead it is {1}".format(correct_x_opt,x_opt)
            self.fail(error_msg)
        # Check that it optimized correctly the f_opt
        correct_f_opt = 0
        if not numpy.isclose(correct_f_opt,f_opt,atol=epsilon):
            error_msg = "f(x) should be close to {0}" \
                        " but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)



    # Auxs
    def threeParamsModelOptimizerBaseArgsExample(self):
        model_name = "Model"
        model_file_path = os.path.join(self._temp_dir, "model.mo")
        files_aux.writeStrToFile(model_str, model_file_path)
        start_time = 0
        stop_time = 2
        target_var_name = "x"
        parameters_to_perturb = ["a", "b", "c"]
        lower_bounds = [-2, -2, -2]
        upper_bounds = [ 2,  2,  2]
        max_or_min = "min"
        epsilon = 0.001
        build_folder_path = self._temp_dir
        return model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb,\
               lower_bounds, upper_bounds, max_or_min, epsilon, build_folder_path





###########
# Globals #
###########
model_str = \
 """class Model
  parameter Real a=1;
  parameter Real b=1;
  parameter Real c=1;
  Real x(fixed=true);
equation
  der(x) = a+b+c;
end Model;"""
