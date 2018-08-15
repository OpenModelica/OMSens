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

    def test_indiv_sens_predefined_tests_are_all_valid_without_running(self):
        # Get path of where tests are
        project_root_path = filesystem.files_aux.projectRoot()
        test_files_folder_path = os.path.join(project_root_path, "resource", "experiments", "individual")
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
