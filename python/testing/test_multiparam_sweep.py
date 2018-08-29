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
import running.sweep
import filesystem.files_aux as files_aux


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
    def test_values_subtests(self):
        # We add several tests in one because we have to build the model each time so we avoid doing it here
        # Initialize sweep example
        sweep_runner = self.sweepSpecsExample()
        # Test that the values per param are correct
        # Get values for each param
        vals_per_param = sweep_runner.valuesPerParameter()
        correct_vals_per_param = {
            "a": [-1],
            "b": [-0.9, -1.1],
            "c": [-0.85, -1, -1.15],
        }
        for p in correct_vals_per_param:
            p_vals = vals_per_param[p]
            p_correct_vals = correct_vals_per_param[p]
            for v1, v2 in zip(p_vals, p_correct_vals):
                if not v1 == v2:
                    error_msg = "The parameter '{0}' has val {1} when it should have val {2}".format(p, v1, v2)
                    self.fail(error_msg)
        # Test that the number of combinations are correct
        vals_combinations_n = len(list(sweep_runner.parametersValuesCombinationsGenerator()))
        correct_n_runs = 6
        if vals_combinations_n != correct_n_runs:
            error_msg = "The sweep should have {0} runs but it had {1}".format(vals_combinations_n, correct_n_runs)
            self.fail(error_msg)
        # Test that the sweep "works"
        sweep_results = sweep_runner.runSweep(self._temp_dir)
        # Check that the swept params are correct
        swept_params = sweep_results.swept_parameters_names
        correct_swept_params = list(correct_vals_per_param.keys())
        intersection_swept_params = [i for i,j in zip(swept_params, correct_swept_params) if i == j]
        if len(intersection_swept_params) != 3:
            error_msg = "The swept params returned were {0} when they should've been {1}".format(swept_params, correct_swept_params)
            self.fail(error_msg)
        # Check that there is a file in the std run path
        std_run = sweep_results.std_run
        std_run_path = pathlib.Path(std_run.output_path)
        if not std_run_path.is_file():
            error_msg = "The std run was not found in path {0}".format(std_run_path.absolute())
            self.fail(error_msg)
        # Check that there is a file for each perturbed run
        perturbed_runs = sweep_results.perturbed_runs
        for pert_run in perturbed_runs:
            pert_run_path = pathlib.Path(pert_run.simulation_results.output_path)
            if not pert_run_path.is_file():
                error_msg = "A perturbed run was not found in path {0}".format(pert_run_path.absolute())
                self.fail(error_msg)


    # Auxs
    def sweepSpecsExample(self):
        model_name = "Model"
        model_file_path = os.path.join(self._temp_dir, "model.mo")
        files_aux.writeStrToFile(model_str, model_file_path)
        start_time = 0
        stop_time = 2
        perturbation_info_per_param = [
            {
                "name": "a",
                "delta_percentage": 5,
                "iterations": 1
            },
            {
                "name": "b",
                "delta_percentage": 10,
                "iterations": 2
            },
            {
                "name": "c",
                "delta_percentage": 15,
                "iterations": 3
            },
        ]
        sweep_runner = running.sweep.ParametersSweeper(model_name, model_file_path, start_time, stop_time,
                                                       perturbation_info_per_param, self._temp_dir)
        return sweep_runner




###########
# Globals #
###########
model_str = \
    """class Model
      parameter Real a=-1;
      parameter Real b=-1;
      parameter Real c=-1;
      Real x(start=1,fixed=true);
    equation
      der(x) = a*x + b/2 + c/4;
    end Model;"""
