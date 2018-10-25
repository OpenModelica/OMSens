# Std
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
import os
import re

# Mine
from plotting.plot_vectorial import VectorialPlotter
import vectorial.optimization_result as optimization_result_f




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
    def test_plot_sweep_creates_files_in_folder(self):
        # Create an example sweep
        optim_res = self.optimizationResultsExample()
        # Initialize sweep plotter
        sweep_plotter = VectorialPlotter(optim_res)
        # Plot sweep specs to temp folder
        sweep_plotter.plotInFolder(self._temp_dir)
        # Get plots extensions regex
        regex = '.*\.(png|svg)$'
        # Get list of files from regex
        files_in_dir = os.listdir(self._temp_dir)
        plot_files = [x for x in files_in_dir if re.match(regex, x)]
        # Check that there is at least one plot
        if len(plot_files) < 1:
            error_msg = "The plot function should create at least one plot file in the destination folder."
            self.fail(error_msg)


    # Auxs:
    def optimizationResultsExample(self):
        # Optimization results info
        optim_res = optimization_result_f.ModelOptimizationResult(
            f_x0          = 9,
            f_x_opt       = 12,
            stop_time     = 3,
            variable_name = "x",
            x0            = {"a":1},
            x_opt         = {"a":2},
        )
        return optim_res
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

