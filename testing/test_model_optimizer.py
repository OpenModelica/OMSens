# Std
import os
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
import numpy
import pytest

# Mine
import filesystem.files_aux as files_aux
import vectorial.model_optimizer as model_optimizer_f


class TestVectorialSensitivityAnalysis(unittest.TestCase):
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
               percentage, max_or_min, epsilon, build_folder_path = \
            self.threeParamsModelOptimizerBaseArgsExample()
        # Replace the args so we only minimize one
        parameters_to_perturb = ["a"]
        percentage = 300

        # Initialize optimizer
        model_optimizer = model_optimizer_f.ModelOptimizer(model_name, start_time, stop_time, model_file_path,
                                                           target_var_name, parameters_to_perturb, max_or_min,
                                                           build_folder_path)
        # Run optimizer
        optim_result = model_optimizer.optimize(percentage, epsilon)
        x_opt_dict, f_opt = optim_result.x_opt, optim_result.f_x_opt
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
        # Check x0
        correct_x0 = [1]
        optim_x0 = optim_result.x0
        for p_name, correct_val in zip(optim_x0,correct_x0):
            val = optim_x0[p_name]
            if not numpy.isclose(val,correct_val):
                error_msg = "x0: the value {0} should be {1}".format(val,correct_val)
                self.fail(error_msg)
        # Check f(x0)
        correct_f_x0 = 9
        optim_f_x0 = optim_result.f_x0
        if not numpy.isclose(optim_f_x0, correct_f_x0):
            error_msg = "f(x0): the value {0} should be {1}".format(optim_f_x0,correct_f_x0)
            self.fail(error_msg)
        # Check stoptime
        correct_stoptime = 3
        optim_stoptime = optim_result.stop_time
        if not numpy.isclose(optim_stoptime, correct_stoptime):
            error_msg = "stoptime: the value {0} should be {1}".format(optim_stoptime,correct_stoptime)
            self.fail(error_msg)
        # Check variable name
        correct_varname = "x"
        optim_varname = optim_result.variable_name
        if not optim_varname == correct_varname:
            error_msg = "var name: the value {0} should be {1}".format(optim_varname,correct_varname)
            self.fail(error_msg)


    @pytest.mark.slow
    def test_one_param_max(self):
        # Get the base arguments for the 3 params example
        model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb, \
        percentage, max_or_min, epsilon, build_folder_path = \
            self.threeParamsModelOptimizerBaseArgsExample()
        # Replace the args so we only maximize one
        parameters_to_perturb = ["a"]
        percentage = 100
        max_or_min = "max"
        # Initialize optimizer
        model_optimizer = model_optimizer_f.ModelOptimizer(model_name, start_time, stop_time, model_file_path,
                                                           target_var_name, parameters_to_perturb, max_or_min,
                                                           build_folder_path)
        # Run optimizer
        optim_result = model_optimizer.optimize(percentage, epsilon)
        x_opt_dict, f_opt = optim_result.x_opt, optim_result.f_x_opt
        # Check that it optimized correctly the X
        correct_x_opt = 2
        x_opt = x_opt_dict["a"]
        if not numpy.isclose(correct_x_opt,x_opt,atol=epsilon):
            error_msg = "x_opt distance should be close to {0}" \
                        " but instead it is {1}".format(correct_x_opt,x_opt)
            self.fail(error_msg)
        # Check that it optimized correctly the f_opt
        correct_f_opt = 12
        if not numpy.isclose(correct_f_opt,f_opt,atol=epsilon):
            error_msg = "f(x) should be close to {0}" \
                        " but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)

    @pytest.mark.slow
    def test_multiple_params(self):
        # Get the base arguments for the 3 params example
        model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb, \
        percentage, max_or_min, epsilon, build_folder_path = \
            self.threeParamsModelOptimizerBaseArgsExample()
        # Initialize optimizer
        model_optimizer = model_optimizer_f.ModelOptimizer(model_name, start_time, stop_time, model_file_path,
                                                           target_var_name, parameters_to_perturb, max_or_min,
                                                           build_folder_path)
        # Run optimizer
        percentage = 300
        optim_result = model_optimizer.optimize(percentage, epsilon)
        x_opt_dict, f_opt = optim_result.x_opt, optim_result.f_x_opt
        # Check that it optimized correctly the X
        correct_x_opt_dict = {p:-2 for p in ["a", "b", "c"]}
        x_distance_to_correct_x = sum([x_opt_dict[p] - correct_x_opt_dict[p] for p in x_opt_dict])
        if not numpy.isclose(x_distance_to_correct_x,0,atol=epsilon):
            error_msg = "x_opt is not close enough to the correct values. Distance: {0}" \
                        .format(x_distance_to_correct_x)
            self.fail(error_msg)
        # Check that it optimized correctly the f_opt
        correct_f_opt = -18
        if not numpy.isclose(correct_f_opt,f_opt,atol=epsilon):
            error_msg = "f(x) should be close to {0}" \
                        " but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)

    @pytest.mark.slow
    def test_lower_bounds_work(self):
        # Get the base arguments for the 3 params example
        model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb, \
        percentage, max_or_min, epsilon, build_folder_path = \
            self.threeParamsModelOptimizerBaseArgsExample()
        # Replace the args so we only minimize one
        parameters_to_perturb = ["a"]
        percentage = 400
        # Initialize optimizer
        model_optimizer = model_optimizer_f.ModelOptimizer(model_name, start_time, stop_time, model_file_path,
                                                           target_var_name, parameters_to_perturb, max_or_min,
                                                           build_folder_path)
        # Run optimizer
        optim_result = model_optimizer.optimize(percentage, epsilon)
        x_opt_dict, f_opt = optim_result.x_opt, optim_result.f_x_opt
        # Check that it optimized correctly the X
        correct_x_opt = -3
        x_opt = x_opt_dict["a"]
        if not numpy.isclose(correct_x_opt,x_opt,atol=epsilon):
            error_msg = "x_opt distance should be close to {0}" \
                        " but instead it is {1}".format(correct_x_opt,x_opt)
            self.fail(error_msg)

    @pytest.mark.slow
    def test_upper_bounds_work(self):
        # Get the base arguments for the 3 params example
        model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb, \
        percentage, max_or_min, epsilon, build_folder_path = \
            self.threeParamsModelOptimizerBaseArgsExample()
        # Replace the args so we only minimize one
        parameters_to_perturb = ["a"]
        max_or_min = "max"
        percentage = 300
        # Initialize optimizer
        model_optimizer = model_optimizer_f.ModelOptimizer(model_name, start_time, stop_time, model_file_path,
                                                           target_var_name, parameters_to_perturb, max_or_min,
                                                           build_folder_path)
        # Run optimizer
        optim_result = model_optimizer.optimize(percentage, epsilon)
        x_opt_dict, f_opt = optim_result.x_opt, optim_result.f_x_opt
        # Check that it optimized correctly the X
        correct_x_opt = 4
        x_opt = x_opt_dict["a"]
        if not numpy.isclose(correct_x_opt,x_opt,atol=epsilon):
            error_msg = "x_opt distance should be close to {0}" \
                        " but instead it is {1}".format(correct_x_opt,x_opt)
            self.fail(error_msg)

    # IMPORTANT!: the following test depends on CURVI's implementation! If by "chance" it finds the optimum in one of
    #  the iterations, then the epsilon to choose is irrelevant. BE CAREFUL WITH HOW TO INTERPRET THE FAILS OF THIS
    #  TEST!
    @pytest.mark.slow
    def test_epsilon_works(self):
        # Get the base arguments for the 3 params example
        model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb, \
        percentage, max_or_min, epsilon, build_folder_path = \
            self.threeParamsModelOptimizerBaseArgsExample()
        # Replace the args so we only minimize one
        parameters_to_perturb = ["d"]
        percentage = 1000
        target_var_name = "y"
        # Initialize optimizer
        model_optimizer = model_optimizer_f.ModelOptimizer(model_name, start_time, stop_time, model_file_path,
                                                           target_var_name, parameters_to_perturb, max_or_min,
                                                           build_folder_path)
        # Run optimizer with permissive epsilon
        epsilon_permissive = 0.1
        optim_result_permissive = model_optimizer.optimize(percentage, epsilon_permissive)
        x_opt_dict_permissive, f_opt_permissive = optim_result_permissive.x_opt, optim_result_permissive.f_x_opt
        # Run optimizer with strict epsilon
        epsilon_strict = 0.0001
        optim_result_strict = model_optimizer.optimize(percentage, epsilon_strict)
        x_opt_dict_strict, f_opt_strict = optim_result_strict.x_opt, optim_result_strict.f_x_opt
        # Check that it optimized correctly the X
        x_opt_distance_permissive = abs(x_opt_dict_permissive["d"])
        x_opt_distance_strict     = abs(x_opt_dict_strict["d"])
        if not x_opt_distance_strict < x_opt_distance_permissive:
            error_msg = "The strict X should be closer to the correct value than the permissive. " \
                        "distance permissive: {0}. distance strict: {1}".format(x_opt_distance_permissive, x_opt_distance_strict)
            self.fail(error_msg)

    # Auxs
    def threeParamsModelOptimizerBaseArgsExample(self):
        model_name = "Model"
        model_file_path = os.path.join(self._temp_dir, "model.mo")
        files_aux.writeStrToFile(model_str, model_file_path)
        start_time = 0
        stop_time = 3
        target_var_name = "x"
        parameters_to_perturb = ["a", "b", "c"]
        percentage = 5
        max_or_min = "min"
        epsilon = 0.001
        build_folder_path = self._temp_dir
        return model_name, start_time, stop_time, model_file_path, target_var_name, parameters_to_perturb,\
               percentage, max_or_min, epsilon, build_folder_path





###########
# Globals #
###########
model_str = \
 """class Model
  parameter Real a=1;
  parameter Real b=1;
  parameter Real c=1;
  parameter Real d=1;
  Real x;
  Real y;
equation
  der(x) = a+b+c;
  y = d^2;
end Model;"""
