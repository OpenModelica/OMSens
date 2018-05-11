# Standard
import os
import shutil
import tempfile
import unittest

import filesystem.files_aux
import mos_writer.calculate_sensitivities_mos_writer as sens_mos_writer
# Ours
import running.run_omc as omc_runner
from settings import settings_world3_sweep as world3_settings


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

    def test_creates_and_runs_indiv_sens_mos_script_correctly(self):
        # Write simple model to temp dir
        mo_file_name = "model.mo"
        mo_file_path = os.path.join(self._temp_dir, mo_file_name)
        filesystem.files_aux.writeStrToFile(model_str, mo_file_path)
        # Define names and paths for the other things
        output_mos_name = "script.mos"
        output_mos_path = os.path.join(self._temp_dir, output_mos_name)
        std_run_filename = "std_run.csv"
        # Prepare mos creator arguments
        mos_creator_kwargs = {
            "model_name": "Model",
            "mo_file": mo_file_path,
            "startTime": 0,
            "stopTime": 2,
            "parameters_to_perturbate_tuples": [("a", -1, 5)],
            "output_mos_path": output_mos_path,
            "csv_file_name_modelica_function": world3_settings.calc_sens_csv_file_name_function,
            "std_run_filename": std_run_filename,
        }
        # Call .mos creator
        sens_mos_writer.createMos(**mos_creator_kwargs)
        process_output = omc_runner.runMosScript(output_mos_path)
        error_line = process_output.splitlines()[-1]
        self.assertEqual(error_line, 'true')


model_str = \
    """
    class Model
      parameter Real a=-1;
      Real x(start=1,fixed=true);
    equation
      der(x) = a*x;
    end Model;
    """
