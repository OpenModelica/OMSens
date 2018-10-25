# Std
import glob
import os
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
import pathlib
import pandas
import numpy

# Mine
import running.sweep
import filesystem.files_aux as files_aux
import plotting.plot_sweep as plot_sweep


class TestMultiparameterSweep(unittest.TestCase):
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
            "a": [-0.95, -1.05],
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
        vals_combinations_n = len(list(sweep_runner.runsPerturbedParameters()))
        correct_n_runs = 12
        if vals_combinations_n != correct_n_runs:
            error_msg = "The sweep should have {0} runs but it had {1}".format(correct_n_runs, vals_combinations_n)
            self.fail(error_msg)
        # Test that the sweep "works"
        sweep_results = sweep_runner.runSweep(self._temp_dir)
        # Check that the swept params are correct<
        swept_params = sweep_results.swept_parameters_names
        correct_swept_params = list(correct_vals_per_param.keys())
        intersection_swept_params = [i for i,j in zip(swept_params, correct_swept_params) if i == j]
        if len(intersection_swept_params) != 3:
            error_msg = "The swept params returned were {0} when they should've been {1}".format(swept_params, correct_swept_params)
            self.fail(error_msg)
        # Check that the std run has the correct values
        variables = ["xa", "xb", "xc", "y"]
        vars_std_val = -1
        std_run = sweep_results.std_run
        std_run_path = std_run.output_path
        df_std = pandas.read_csv(std_run_path,index_col=0)
        df_std_last_row = df_std.iloc[-1]
        for var in variables:
            var_val = df_std_last_row[var]
            if not numpy.isclose(var_val, vars_std_val):
                error_msg = "The variable {0} should have value {1} but it has value {2} standard run" \
                    .format(var, vars_std_val, var_val)
                self.fail(error_msg)
        # Define matches between parameters and variables in the model
        param_var_match = {
            "a" : "xa",
            "b" : "xb",
            "c" : "xc",
            "d" : "y",
        }
        # Save the fixed params info
        fixed_params = sweep_results.fixed_parameters_info
        # Check that the perturbed runs have the correct values
        perturbed_runs = sweep_results.perturbed_runs
        for pert_run in perturbed_runs:
            # Get run .csv path
            run_csv_path  = pert_run.simulation_results.output_path
            # Get df for run simulation
            df_pert_run = pandas.read_csv(run_csv_path, index_col=0)
            df_last_row = df_pert_run.iloc[-1]
            params_info_pert_run = pert_run.swept_params_info
            for param_info in params_info_pert_run:
                p_name = param_info.name
                var_for_param = param_var_match[p_name]
                p_new_val = param_info.new_val
                df_var_val = df_last_row[var_for_param]
                if not numpy.isclose(df_var_val, p_new_val):
                    error_msg = "The variable {0} should have value {1} but it has value {2} in run with path {3}"\
                        .format(var_for_param, p_new_val, df_var_val, run_csv_path)
                    self.fail(error_msg)
            # Check the fixed params
            for fixed_p in fixed_params:
                p_name = fixed_p.name
                var_for_param = param_var_match[p_name]
                p_new_val = fixed_p.new_val
                df_var_val = df_last_row[var_for_param]
                if not numpy.isclose(df_var_val, p_new_val):
                    error_msg = "The variable {0} should have value {1} but it has value {2} in run with path {3}" \
                        .format(var_for_param, p_new_val, df_var_val, run_csv_path)
                    self.fail(error_msg)
        # Integration test: we take advantage of the model build and sweep in this test and we test integration
        plot_folder_path = os.path.join(self._temp_dir, "plots")
        files_aux.makeFolderWithPath(plot_folder_path)
        sweep_plotter = plot_sweep.SweepPlotter(sweep_results)
        sweep_plotter.plotInFolder("xa",plot_folder_path)
        # Check that the plots folder is not empty
        files_in_dir = os.listdir(plot_folder_path)
        if len(files_in_dir) < 1:
            error_msg = "The sweep + plot didn't make any files in dest folder"
            self.fail(error_msg)


    # Auxs
    def sweepSpecsExample(self):
        model_name = "Model"
        model_file_path = os.path.join(self._temp_dir, "model.mo")
        files_aux.writeStrToFile(model_str, model_file_path)
        start_time = 0
        stop_time = 1
        fixed_params = [{"name":"d", "value":1}]
        perturbation_info_per_param = [
            {
                "name": "a",
                "delta_percentage": 5,
                "iterations": 2
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
                                                       perturbation_info_per_param, fixed_params, self._temp_dir,
                                                       number_of_intervals=2)
        return sweep_runner




###########
# Globals #
###########
model_str = \
    """class Model
      parameter Real a=-1;
      parameter Real b=-1;
      parameter Real c=-1;
      parameter Real d=-1;
      Real xa;
      Real xb;
      Real xc;
      Real y;
    equation
      der(xa) = a;
      der(xb) = b;
      der(xc) = c;
      der(y)  = d;
    end Model;"""
