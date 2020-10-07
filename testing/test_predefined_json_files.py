# Standard
import os
import re
import shutil
import tempfile
import unittest

import pytest

import filesystem.files_aux
import multiparam_sweep
import individual_sens_calculator


class TestsPredefinedJSONFiles(unittest.TestCase):
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

    @pytest.mark.slow
    def test_run_all_indiv_sens_json_files(self):
        # Get path of where tests are
        project_root_path = filesystem.files_aux.projectRoot()
        test_files_folder_path = os.path.join(project_root_path, "resource", "experiments", "individual")
        for test_file_name in os.listdir(test_files_folder_path):
            json_file_path = os.path.join(test_files_folder_path, test_file_name)
            if os.path.isfile(json_file_path):
                try:
                    individual_sens_calculator.perturbateAndAnalyzeFromJsonToPath(json_file_path, self._temp_dir)
                    print("1. Calling ls -lh {0}".format(self._temp_dir))
                    print(os.system("ls -lh {0}".format(self._temp_dir)))
                    # Remove every file so the next test has the folder clean
                    regex = '.*'
                    filesystem.files_aux.removeFilesWithRegexAndPath(regex, self._temp_dir)
                    print("2. Calling ls -lh {0}".format(self._temp_dir))
                    print(os.system("ls -lh {0}".format(self._temp_dir)))
                except Exception as e:
                    error_msg = str(e)
                    print("3. Calling ls -lh {0}".format(self._temp_dir))
                    print(os.system("ls -lh {0}".format(self._temp_dir)))
                    if os.path.isfile("{0}/omc_run_log.txt".format(self._temp_dir)):
                        f = open("{0}/omc_run_log.txt".format(self._temp_dir), "r")
                        print(f.read())
                    else:
                        print("Failed to read the omc_run_log.txt file. No such file exist.")
                    self.fail("The file {0} is an invalid test file. It raised the following exception:\n {1}".format(
                        json_file_path, error_msg))


    @pytest.mark.slow
    def test_run_all_sweep_JSON_files(self):
        # Get path of where tests are
        project_root_path = filesystem.files_aux.projectRoot()
        exp_files_folder_path = os.path.join(project_root_path, "resource", "experiments", "sweep")
        # General settings for mos creation
        for exp_file_name in os.listdir(exp_files_folder_path):
            exp_file_path = os.path.join(exp_files_folder_path, exp_file_name)
            if os.path.isfile(exp_file_path):
                try:
                    multiparam_sweep.sweepAndPlotFromJSON(self._temp_dir,exp_file_path)
                    print("4. Calling ls -lh {0}".format(self._temp_dir))
                    print(os.system("ls -lh {0}".format(self._temp_dir)))
                    # Remove every file so the next test has the folder clean
                    regex = '.*'
                    filesystem.files_aux.removeFilesWithRegexAndPath(regex, self._temp_dir)
                    print("5. Calling ls -lh {0}".format(self._temp_dir))
                    print(os.system("ls -lh {0}".format(self._temp_dir)))
                except Exception as e:
                    error_msg = str(e)
                    print("6. Calling ls -lh {0}".format(self._temp_dir))
                    print(os.system("ls -lh {0}".format(self._temp_dir)))
                    if os.path.isfile("{0}/omc_run_log.txt".format(self._temp_dir)):
                        f = open("{0}/omc_run_log.txt".format(self._temp_dir), "r")
                        print(f.read())
                    else:
                        print("Failed to read the omc_run_log.txt file. No such file exist.")
                    self.fail("The file {0} is an invalid test file. It raised the following exception:\n {1}".format(
                        exp_file_path, error_msg))                    
