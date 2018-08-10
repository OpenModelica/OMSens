# Std
import glob
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
from io import StringIO
import pandas
import os

import numpy

# Mine
import analysis.indiv_sens
import filesystem.files_aux
from running.simulation_run_info import SimulationRunInfo


class TestSweepPlot(unittest.TestCase):
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
    def test_plot_sweep_doesnt_raise_errors(self):
        # Read standard run
        df_std_run = pandas.read_csv(StringIO(bb_std_run_str), index_col=0)
        # Simulate perturbations by multiplying variables
        runs = []
        for i in range(1, 9):
            df_perturbed_i = df_std_run.copy()
            df_perturbed_i["v"] = df_perturbed_i.apply(lambda row: row["v"] * (1 + i / 8), axis=1)
            run_output_name = "run_{0}.csv".format(i)
            run_output_path = os.path.join(self._temp_dir, run_output_name)
            df_perturbed_i.to_csv(run_output_path)
            # Pretend that e is always changed to 1 and g is swept in each run
            run_parameters_changed = {
                "e": 1,
                "g": i,
            }
            run_model_name = "BouncingBall"
            # The executable can be anything as we asume it has already been ran
            run_executable = "/path/to/exe"
            run = SimulationRunInfo(run_output_path, run_parameters_changed, run_model_name, run_executable)


###########
# Globals #
###########
bb_std_run_str = \
    """"time","h","v","der(h)","der(v)","v_new","flying","impact"
    0,1,0,0,-9.81,0,1,0
    1,0.2250597607429705,-2.279940238910565,-2.279940238910565,-9.81,3.100612842801532,1,0
    2,0.04243354772647411,-0.5463586255141026,-0.5463586255141026,-9.81,1.063510205007515,1,0
    3,2.101988323055078e-11,0,0,0,0,0,1"""
