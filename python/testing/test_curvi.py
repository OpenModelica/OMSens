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
import plotting.plot_sweep as plot_sweep


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
    def test_curvi_finds_minimum_of_cuadratic(self):
        curvi_mod = self.tryToImportCurviModule()
        x0, obj_func, epsilon = cuadraticFuncArgs()
        lower_bounds = [-2]
        upper_bounds = [2]
        x_opt,f_opt = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon)
        correct_x_opt = [0]
        if not numpy.isclose(x_opt,correct_x_opt):
            error_msg = "x_opt should be close to {0} but instead it is {1}".format(correct_x_opt,x_opt)
            self.fail(error_msg)
        correct_f_opt = 0
        if not numpy.isclose(f_opt,correct_f_opt):
            error_msg = "f_opt should be close to {0} but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)

    def test_curvi_bounds_work(self):
        curvi_mod = self.tryToImportCurviModule()
        x0, obj_func, epsilon = cuadraticFuncArgs()
        lower_bounds = [0.5]
        upper_bounds = [1]
        x_opt,f_opt = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon)
        correct_x_opt = [0.5]
        if not numpy.isclose(x_opt,correct_x_opt):
            error_msg = "x_opt should be close to {0} but instead it is {1}".format(correct_x_opt,x_opt)
            self.fail(error_msg)
        correct_f_opt = 0.25
        if not numpy.isclose(f_opt,correct_f_opt,0.0001):
            error_msg = "f_opt should be close to {0} but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)

    # Auxs:
    def tryToImportCurviModule(self):
        try:
            import fortran_interface.curvif_simplified as curvif_simplified
        except:
            error_msg = "The curvi optimizer was not installed correctly and is unavailable"
            self.fail(error_msg)
        return curvif_simplified


def cuadraticFuncArgs():
    x0 = numpy.array([1])
    obj_func = lambda x: x**2
    epsilon = 0.0001
    return x0, obj_func, epsilon
