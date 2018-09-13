# Standard
import os
import re
import shutil
import tempfile
import unittest

import pytest

import analysis.indiv_sens
import filesystem.files_aux
import mos_writer.calculate_sensitivities_mos_writer as sens_mos_writer
# Ours
import modelica_interface.run_omc as omc_runner


class TestsRunOMC(unittest.TestCase):
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

    # This test is commented because it's for when we used mos scripts
    # @pytest.mark.slow
    # def test_indiv_sens_from_json_with_correct_data_simulates_and_analyzescorrectly(self):
    #     # Write simple model to temp dir
    #     mo_file_name = "model.mo"
    #     mo_file_path = os.path.join(self._temp_dir, mo_file_name)
    #     filesystem.files_aux.writeStrToFile(model_str, mo_file_path)
    #     # Define names and paths for the other things
    #     output_mos_name = "script.mos"
    #     output_mos_path = os.path.join(self._temp_dir, output_mos_name)
    #     std_run_filename = "std_run.csv"
    #     # Set json string dynamically
    #     valid_json_str = valid_json_skeleton.format(mo_file_path=mo_file_path)
    #     # We have to write the json to file because for some reason the StringIO wrapper isn't working here
    #     json_file_path = os.path.join(self._temp_dir, "test.json")
    #     filesystem.files_aux.writeStrToFile(valid_json_str, json_file_path)
    #     # Create mos from JSON info
    #     mos_info = sens_mos_writer.createMosFromJSON(json_file_path, output_mos_path, std_run_filename)
    #     process_output = omc_runner.runMosScript(output_mos_path)
    #     error_line = process_output.splitlines()[-1]
    #     # Assert that the script ends without error
    #     self.assertEqual(error_line, '""', msg="The last line of the .mos execution was not satisfactory. It ended "
    #                                              "with an unexpected output.")
    #     # Assert that there's a file containing the substring of the param of the model in the temp dir
    #     files_matching_regex = []
    #     for x in os.listdir(self._temp_dir):
    #         # Get the list of files with filename containing the param name
    #         if re.match('.*param_name.*\.csv$', x):
    #             files_matching_regex.append(x)
    #     if len(files_matching_regex) != 1:
    #         if len(files_matching_regex) > 1:
    #             error_msg = "There is more than one CSV file matching with the param_name."
    #             self.fail(error_msg)
    #         if len(files_matching_regex) < 1:
    #             error_msg = "We couldn't find the CSV file with the param perturbed run results. Check that the " \
    #                         "executable could be run (make sure /tmp is executable) "
    #             self.fail(error_msg)
    #     # We also test here that the consequent analysis works. It's not the best programming practice but because
    #     #   it may be too much consuming depending on hardware, we take advantage of the simulation in this test.
    #     # Prepare analysis inputs
    #     mos_perturbed_runs_info = mos_info["perturbed_runs"]
    #     # Get standard run simulation results file name and get its path using the temp dir
    #     std_run_csv_name = mos_info["std_run_file_name"]
    #     std_run_csv_path = os.path.join(self._temp_dir,std_run_csv_name)
    #     analyze_csvs_kwargs = {
    #         "perturbed_simus_info"             : mos_perturbed_runs_info,
    #         "std_run_csv_path"                  : std_run_csv_path,
    #         "target_vars"                       : ['x'],
    #         "percentage_perturbed"              : 5,
    #         "specific_year"                     : 3,
    #         "output_folder_analyses_path"       : self._temp_dir,
    #         "rms_first_year"                    : 0,
    #         "rms_last_year"                     : 3,
    #     }
    #     # We only test that it doesn't raise an error. The functional test is in its respective test class
    #     analysis_files_paths = analysis.indiv_sens.completeIndividualSensAnalysis(**analyze_csvs_kwargs)


# The following test requires that we test by hand if the parameter exists or not. OM doesn't fail if we try to set
#  a parameter that doesn't exist
# def test_indiv_sens_from_json_fails_if_incorrect_param_name(self):
#   pass

# Data used for testing
model_str = \
    """
    class Model
      parameter Real param_name=-1;
      Real x(start=1,fixed=true);
    equation
      der(x) = param_name*x;
    end Model;
    """
valid_json_skeleton = \
    """{{
       "model_name": "Model",
       "model_mo_path": "{mo_file_path}",
       "percentage":5,
       "start_time":0,
       "stop_time":3,
       "vars_to_analyze":["x"],
       "params_info_list": [
           {{
               "name":"param_name",
               "initial_val":-1
           }}
       ]
    }}"""
