#Std
import glob
import os
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
from io import StringIO
import pathlib

import numpy

# Mine
import analysis.indiv_sens as indiv_sens
import filesystem.files_aux as files_aux
from callable_methods import individual_sens_calculator
import running.simulation_run_info as simu_run_info


class TestIndividualSensitivityAnalysis(unittest.TestCase):
#setup y teardown de los tests
    def setUp(self):
        #Create tempdir and save its path
        self._temp_dir = tempfile.mkdtemp()
        # each test case can create individual files
        self._temp_files = []

    def tearDown(self):
        pass
        shutil.rmtree(self._temp_dir)
        for f in self._temp_files:
            f.close()

# Aux model
    def isolatedPerturbationModelExample(self):
        build_folder_path, model_file_path, model_name, parameters_to_perturb, perc_perturb, start_time, stop_time = \
            self.modelExample()
        # Initialize param perturber
        params_perturbator = indiv_sens.ParametersIsolatedPerturbator(model_name, model_file_path, start_time,
                                                                      stop_time, parameters_to_perturb, perc_perturb,
                                                                      build_folder_path)
        return params_perturbator

    def modelExample(self):
        model_name = "Model"
        model_file_path = os.path.join(self._temp_dir, "model.mo")
        files_aux.writeStrToFile(model_str, model_file_path)
        start_time = 0
        stop_time = 2
        parameters_to_perturb = ["a", "b", "c"]
        perc_perturb = 5
        build_folder_path = self._temp_dir
        return build_folder_path, model_file_path, model_name, parameters_to_perturb, perc_perturb, start_time, stop_time

# Tests:
    def test_multiple_tests(self):
        # Get perturbation for test example
        params_perturbator = self.isolatedPerturbationModelExample()
        # Get vals to be used per parameter in the simulations
        values_per_param = params_perturbator.values_per_param
        # Test that the values are correct
        correct_vals_per_param = {
            "a": -1.05,
            "b": -1.05,
            "c": -1.05,
        }
        for param in correct_vals_per_param:
            val = values_per_param[param]
            correct_val = correct_vals_per_param[param]
            if not numpy.isclose(val, correct_val):
                error_msg = "The perturbed value {0} should be {1} but it isn't.".format(val, correct_val)
                self.fail(error_msg)
        # Test that the run creates at least one .csv
        isolated_perturbations_results = params_perturbator.runSimulations(self._temp_dir)
        csv_files = list(glob.iglob(self._temp_dir + '/**/*.csv', recursive=True))
        if len(csv_files) < 1:
            error_msg = "The run should've created at list one CSV file and it didn't."
            self.fail(error_msg)
        # Check that there is a file in the std run path
        std_run = isolated_perturbations_results.std_run
        std_run_path = pathlib.Path(std_run.output_path)
        if not std_run_path.is_file():
            error_msg = "The std run was not found in path {0}".format(std_run_path.absolute())
            self.fail(error_msg)
        # Check that there is a file for each perturbed run
        runs_per_parameter = isolated_perturbations_results.runs_per_parameter
        for param_name in runs_per_parameter:
            pert_run_info = runs_per_parameter[param_name]
            pert_run_simu_results = pert_run_info.simu_results
            pert_run_path = pathlib.Path(pert_run_simu_results.output_path)
            if not pert_run_path.is_file():
                error_msg = "A perturbed run was not found in path {0}".format(pert_run_path.absolute())
                self.fail(error_msg)
        # Above was for the perturbation, below is for the analysis

    def test_perturbation_and_analysis_integration(self):
        build_folder_path, model_file_path, model_name, parameters_to_perturb, perc_perturb, start_time, stop_time = \
            self.modelExample()
        perturbateAndAnalyze_kwargs = {
            "model_name"            : model_name,
            "model_file_path"       : model_file_path,
            "start_time"            : start_time,
            "stop_time"             : stop_time,
            "parameters_to_perturb" : parameters_to_perturb,
            "percentage"            : perc_perturb,
            "target_vars"           : "x",
            "dest_folder_path"      : build_folder_path,
        }
        individual_sens_calculator.perturbateAndAnalyze(**perturbateAndAnalyze_kwargs)

    def test_sens_run_gives_correct_results(self):
        # Run info. This corresponds to a simulation that perturbed some parameters in isolation. To avoid running the simulation in this test,
        #   we save the simulation's result instead.
        isolated_perturbations_results = validPerturbationExample()
        analyze_csvs_kwargs = {
            "isolated_perturbations_results": isolated_perturbations_results,
            "target_vars"                        : ['h'],
            "percentage_perturbed"               : 5,
            "specific_year"                      : 3,
            "output_folder_analyses_path"        : self._temp_dir,
            "rms_first_year"                     : 0,
            "rms_last_year"                      : 3,
        }
        # Run analysis from simulation info
        analysis_results = indiv_sens.completeIndividualSensAnalysis(**analyze_csvs_kwargs)
        analysis_files_paths = analysis_results["paths"]
        # Test that that the resulting run info includes the basic info: all param names, default and perturbed vals, the variable and its value
        vars_sens_info = analysis_files_paths["vars_sens_info"]
        params_strs = ["e","g"]
        # Method results for the run being tested:
        g_rel_method_per_var = {
            "h": [ "251928", "001858"],
        }
        # Test sens info files
        # Iterate the results testing that they include the necessary information
        # Run info csvs:
        for t_var in analyze_csvs_kwargs["target_vars"]:
            # Read file into memory as str
            run_info_path = vars_sens_info[t_var]
            run_info_str = files_aux.readStrFromFile(run_info_path)
            # Get the list of strings that the file must include
            strs_to_include = params_strs + g_rel_method_per_var[t_var]
            # Check that the strs are included
            for s in strs_to_include:
                if s not in run_info_str:
                    self.fail("The sens info file should but doesn't include the string {0}.".format(s))
        # Test sens matrices files
        methods_correct_vals_tuples = [("Relative", "251928"), ("RMS", "04251")]
        for method_name, str_to_include in methods_correct_vals_tuples:
            # Get path for this method's matrix
            mat_path = analysis_files_paths["heatmaps"][method_name]["matrix_file_path"]
            # Read file into memory as str
            mat_str = files_aux.readStrFromFile(mat_path)
            # Check that the strs are included
            if str_to_include not in mat_str:
                self.fail("The matrix file should but doesn't include the string {0}.".format(str_to_include))
        # Test that the IDs written for heatmap vars and cols include vars and cols, respectively
        vars_names = ["h"]
        param_names = ["g", "e"]
        for method_name in ["Relative", "RMS"]:
            # Get path for this method's IDs
            index_IDs_path = analysis_files_paths["heatmaps"][method_name]["index_mapping_file_path"]
            cols_IDs_path = analysis_files_paths["heatmaps"][method_name]["cols_mapping_file_path"]
            # Read files into memory as str
            index_IDs_str = files_aux.readStrFromFile(index_IDs_path)
            cols_IDs_str = files_aux.readStrFromFile(cols_IDs_path)
            # Check that the strs are included
            for v in vars_names:
                if v not in cols_IDs_str:
                    self.fail("The IDs file {0} should but doesn't include the string {1}.".format(cols_IDs_path, v))
            for param in param_names:
                if param not in index_IDs_str:
                    self.fail(
                        "The IDs file {0} should but doesn't include the string {1}.".format(index_IDs_path, param))
        # Test heatmap files
        heatmap_files = list(glob.iglob(self._temp_dir + '/**/*.png', recursive=True))
        if len(heatmap_files) < 1:
            error_msg = "The run should've created at list one heatmap plot file and it didn't."
            self.fail(error_msg)
        # Test dataframes in memory
        methods_correct_vals_tuples = [("Relative", 0.251928), ("RMS", 0.042515)]
        for method_name, val_to_include in methods_correct_vals_tuples:
            df_method = analysis_results["dfs"]["sens_matrices"][method_name]
            includes_val = numpy.isclose(df_method, val_to_include).any()
            if not includes_val:
                error_msg = "The method {0} does not include the value {1}".format(method_name, val_to_include)
                self.fail(error_msg)

    def test_different_shapes_raises_error(self):
            # For RMS we need all of the simulation results (std run and perturbed runs) to have the same amount of rows.
            # Base kwargs that will be modified for each case:
            analyze_csvs_kwargs_base = {
                "isolated_perturbations_results"     : validPerturbationExample(),
                "target_vars"                        : ['h'],
                "percentage_perturbed"               : 5,
                "specific_year"                      : 3,
                "output_folder_analyses_path"        : self._temp_dir,
                "rms_first_year"                     : 0,
                "rms_last_year"                      : 3,
            }
            # First sub-test: e has 1 more row
            isolated_perturbations_results_1 = eHasOneMoreRowPerturbationExample()
            analyze_csvs_kwargs_1 = analyze_csvs_kwargs_base.copy()
            analyze_csvs_kwargs_1["isolated_perturbations_results"] = isolated_perturbations_results_1
            self.assertRaises(indiv_sens.InvalidSimulationResultsException, indiv_sens.completeIndividualSensAnalysis,
                              **analyze_csvs_kwargs_1)
            # Second sub-test: g has 1 more row
            isolated_perturbations_results_2 = gHasOneMoreRowPerturbationExample()
            analyze_csvs_kwargs_2 = analyze_csvs_kwargs_base.copy()
            analyze_csvs_kwargs_2["isolated_perturbations_results"] = isolated_perturbations_results_2
            self.assertRaises(indiv_sens.InvalidSimulationResultsException, indiv_sens.completeIndividualSensAnalysis,
                              **analyze_csvs_kwargs_2)
            # Third sub-test: std has 1 more row
            isolated_perturbations_results_3 = stdRunHasOneMoreRowPerturbationExample()
            analyze_csvs_kwargs_3 = analyze_csvs_kwargs_base.copy()
            analyze_csvs_kwargs_3["isolated_perturbations_results"] = isolated_perturbations_results_3
            self.assertRaises(indiv_sens.InvalidSimulationResultsException, indiv_sens.completeIndividualSensAnalysis,
                              **analyze_csvs_kwargs_3)

# Auxs
def validPerturbatorInternalresults():
    model_name = "BouncingBall"
    std_run_results = simu_run_info.SimulationResults(StringIO(bb_std_run_str), "BouncingBall", "/path/to/exe",
                                                      "output")
    # Prepare "e" parameter run
    e_perturbed_param_info = simu_run_info.PerturbedParameterInfo("e", 0.7, 0.735)
    e_run_results = simu_run_info.SimulationResults(StringIO(bb_e_perturbed_str), "BouncingBall", "/path/to/exe",
                                                    "output")
    # Prepare "g" parameter run
    g_perturbed_param_info = simu_run_info.PerturbedParameterInfo("g", 9.81, 10.3005)
    g_run_results = simu_run_info.SimulationResults(StringIO(bb_g_perturbed_str), "BouncingBall", "/path/to/exe",
                                                    "output")
    return e_perturbed_param_info, e_run_results, g_perturbed_param_info, g_run_results, model_name, std_run_results


def validPerturbationExample():
    e_perturbed_param_info, e_run_results, g_perturbed_param_info, g_run_results, model_name, std_run_results = validPerturbatorInternalresults()
    e_iter_results = indiv_sens.OneParameterPerturbedResults(e_run_results, e_perturbed_param_info)
    g_iter_results = indiv_sens.OneParameterPerturbedResults(g_run_results, g_perturbed_param_info)
    runs_per_parameter = {
        "e": e_iter_results,
        "g": g_iter_results,
    }
    # Prepare perturbator results using above instances
    isolated_perturbations_results = indiv_sens.IsolatedPerturbationsResults(model_name, std_run_results,
                                                                             runs_per_parameter)
    return isolated_perturbations_results

def eHasOneMoreRowPerturbationExample():
    # Get valid results
    e_perturbed_param_info, e_run_results, g_perturbed_param_info, g_run_results, model_name, std_run_results = validPerturbatorInternalresults()
    # Replace the e run results with invalid results
    e_run_results = simu_run_info.SimulationResults(StringIO(bb_e_perturbed_2_str), "BouncingBall", "/path/to/exe",
                                                    "output")
    # Prepare perturbator results using above instances
    e_iter_results = indiv_sens.OneParameterPerturbedResults(e_run_results, e_perturbed_param_info)
    g_iter_results = indiv_sens.OneParameterPerturbedResults(g_run_results, g_perturbed_param_info)
    runs_per_parameter = {
        "e": e_iter_results,
        "g": g_iter_results,
    }
    isolated_perturbations_results = indiv_sens.IsolatedPerturbationsResults(model_name, std_run_results,
                                                                             runs_per_parameter)
    return isolated_perturbations_results


def gHasOneMoreRowPerturbationExample():
    # Get valid results
    e_perturbed_param_info, e_run_results, g_perturbed_param_info, g_run_results, model_name, std_run_results = validPerturbatorInternalresults()
    # Replace the g run results with invalid results
    g_run_results = simu_run_info.SimulationResults(StringIO(bb_g_perturbed_2_str), "BouncingBall", "/path/to/exe",
                                                    "output")
    # Prepare perturbator results using above instances
    e_iter_results = indiv_sens.OneParameterPerturbedResults(e_run_results, e_perturbed_param_info)
    g_iter_results = indiv_sens.OneParameterPerturbedResults(g_run_results, g_perturbed_param_info)
    runs_per_parameter = {
        "e": e_iter_results,
        "g": g_iter_results,
    }
    isolated_perturbations_results = indiv_sens.IsolatedPerturbationsResults(model_name, std_run_results,
                                                                             runs_per_parameter)
    return isolated_perturbations_results

def stdRunHasOneMoreRowPerturbationExample():
    # Get valid results
    e_perturbed_param_info, e_run_results, g_perturbed_param_info, g_run_results, model_name, std_run_results = validPerturbatorInternalresults()
    # Replace the std run results with invalid results
    std_run_results = simu_run_info.SimulationResults(StringIO(bb_std_run_2_str), "BouncingBall", "/path/to/exe",
                                                      "output")
    # Prepare perturbator results using above instances
    e_iter_results = indiv_sens.OneParameterPerturbedResults(e_run_results, e_perturbed_param_info)
    g_iter_results = indiv_sens.OneParameterPerturbedResults(g_run_results, g_perturbed_param_info)
    runs_per_parameter = {
        "e": e_iter_results,
        "g": g_iter_results,
    }
    isolated_perturbations_results = indiv_sens.IsolatedPerturbationsResults(model_name, std_run_results,
                                                                             runs_per_parameter)
    return isolated_perturbations_results

###########
# Globals #
###########
bb_std_run_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.2250597607429705,-2.279940238910565,-2.279940238910565,-9.81,3.100612842801532,1,0
2,0.04243354772647411,-0.5463586255141026,-0.5463586255141026,-9.81,1.063510205007515,1,0
3,2.101988323055078e-11,0,0,0,0,0,1"""

bb_e_perturbed_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.3100904028764322,-2.124909596770488,-2.124909596770488,-9.81,3.255643484941609,1,0
2,0.04233293611696021,0.9167931152103947,0.9167931152103947,-9.81,1.292703301139997,1,0
3,2.631538447381662e-11,0,0,0,0,0,1"""

bb_g_perturbed_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-10.3005,0,1,0
1,0.1657651633154364,-2.584484836337927,-2.584484836337927,-10.3005,3.177182714449088,1,0
2,0.003483617140901725,-1.056333590801138,-1.056333590801138,-10.3005,1.089773670982276,1,0
3,2.105894579818758e-11,0,0,0,0,0,1"""

bb_std_run_2_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.2250597607429705,-2.279940238910565,-2.279940238910565,-9.81,3.100612842801532,1,0
2,0.04243354772647411,-0.5463586255141026,-0.5463586255141026,-9.81,1.063510205007515,1,0
2.5,0.14243354772647411,-0.5463586255141026,-0.5463586255141026,-9.81,1.063510205007515,1,0
3,2.101988323055078e-11,0,0,0,0,0,1"""

bb_e_perturbed_2_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.3100904028764322,-2.124909596770488,-2.124909596770488,-9.81,3.255643484941609,1,0
2,0.04233293611696021,0.9167931152103947,0.9167931152103947,-9.81,1.292703301139997,1,0
2.5,0.14233293611696021,0.9167931152103947,0.9167931152103947,-9.81,1.292703301139997,1,0
3,2.631538447381662e-11,0,0,0,0,0,1"""

bb_g_perturbed_2_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-10.3005,0,1,0
1,0.1657651633154364,-2.584484836337927,-2.584484836337927,-10.3005,3.177182714449088,1,0
2,0.003483617140901725,-1.056333590801138,-1.056333590801138,-10.3005,1.089773670982276,1,0
2.5,0.103483617140901725,-1.056333590801138,-1.056333590801138,-10.3005,1.089773670982276,1,0
3,2.105894579818758e-11,0,0,0,0,0,1"""

model_str = \
    """class Model
      parameter Real a=-1;
      parameter Real b=-1;
      parameter Real c=-1;
      Real x(start=1,fixed=true);
    equation
      der(x) = a*x + b/2 + c/4;
    end Model;"""
