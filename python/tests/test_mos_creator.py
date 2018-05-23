# Standard
import os
import re
import shutil
import tempfile
import unittest

import io
# Ours
import running.run_omc as omc_runner
import filesystem.files_aux
import mos_writer.calculate_sensitivities_mos_writer as sens_mos_writer


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

    def test_indiv_sens_predefined_tests_are_all_valid(self):
        # Get path of where tests are
        project_root_path = filesystem.files_aux.projectRoot()
        test_files_folder_path = os.path.join(project_root_path, "resource", "test_files", "individual")
        # General settings for mos creation
        output_mos_path = os.path.join(self._temp_dir, "test_script.mos")
        std_run_filename = "std_run.csv"
        for test_file_name in os.listdir(test_files_folder_path):
            test_file_path = os.path.join(test_files_folder_path, test_file_name)
            if os.path.isfile(test_file_path):
                try:
                    mos_file_path = sens_mos_writer.createMosFromJSON(test_file_path, output_mos_path, std_run_filename)
                    # Remove every file so the next test has the folder clean
                    regex = '.*'
                    filesystem.files_aux.removeFilesWithRegexAndPath(regex, self._temp_dir)
                except Exception as e:
                    error_msg = str(e)
                    self.fail("The file {0} is an invalid test file. It raised the following exception:\n {1}".format(
                        test_file_path, error_msg))

    def test_indiv_sens_from_json_with_correct_data_simulates_correctly(self):
        # Write simple model to temp dir
        mo_file_name = "model.mo"
        mo_file_path = os.path.join(self._temp_dir, mo_file_name)
        filesystem.files_aux.writeStrToFile(model_str, mo_file_path)
        # Define names and paths for the other things
        output_mos_name = "script.mos"
        output_mos_path = os.path.join(self._temp_dir, output_mos_name)
        std_run_filename = "std_run.csv"
        # Set json string dynamically
        valid_json_str = valid_json_skeleton.format(mo_file_path=mo_file_path)
        # We have to write the json to file because for some reason the StringIO wrapper isn't working here
        json_file_path = os.path.join(self._temp_dir, "test.json")
        filesystem.files_aux.writeStrToFile(valid_json_str, json_file_path)
        # Prepare mos creator arguments
        sens_mos_writer.createMosFromJSON(json_file_path, output_mos_path, std_run_filename)
        process_output = omc_runner.runMosScript(output_mos_path)
        error_line = process_output.splitlines()[-1]
        # Assert that the script ends without error
        self.assertEqual(error_line, '""', msg="The last line of the .mos execution was not satisfactory. It ended "
                                                 "with an unexpected output.")
        # Assert that there's a file containing the substring of the param of the model in the temp dir
        files_matching_regex = []
        for x in os.listdir(self._temp_dir):
            # Get the list of files with filename containing the param name
            if re.match('.*param_name.*\.csv$', x):
                files_matching_regex.append(x)
        if len(files_matching_regex) != 1:
            if len(files_matching_regex) > 1:
                error_msg = "There is more than one CSV file matching with the param_name."
                self.fail(error_msg)
            if len(files_matching_regex) < 1:
                error_msg = "We couldn't find the CSV file with the param perturbed run results. Check that the " \
                            "executable could be run (make sure /tmp is executable) "
                self.fail(error_msg)


# The following test requires that we test by hand if the parameter exists or not. OM doesn't fail if we try to set
#  a parameter that doesn't exist
# def test_indiv_sens_from_json_fails_if_incorrect_param_name(self):
#   pass

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
