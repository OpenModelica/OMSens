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
        # Get base args for an example function
        x0, obj_func, epsilon, lower_bounds, upper_bounds  = baseCuadraticFuncArgs()
        # Call curvi
        x_opt,f_opt = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon)
        # Check results
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
        x0, obj_func, epsilon , lower_bounds, upper_bounds = baseCuadraticFuncArgs()
        # Redefine the bounds
        lower_bounds = [0.5]
        upper_bounds = [1]
        # Call curvi
        x_opt,f_opt = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon)
        # Check results
        correct_x_opt = [0.5]
        if not numpy.isclose(x_opt,correct_x_opt):
            error_msg = "x_opt should be close to {0} but instead it is {1}".format(correct_x_opt,x_opt)
            self.fail(error_msg)
        correct_f_opt = 0.25
        if not numpy.isclose(f_opt,correct_f_opt, atol=epsilon):
            error_msg = "f_opt should be close to {0} but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)

    # IMPORTANT!: the following test depends on CURVI's implementation! If by "chance" it finds the optimum in one of
    #  the iterations, then the epsilon to choose is irrelevant. BE CAREFUL WITH HOW TO INTERPRET THE FAILS OF THIS
    #  TEST!
    def test_curvi_epsilon_works(self):
        curvi_mod = self.tryToImportCurviModule()
        # Get base args for an example function
        x0, obj_func, epsilon, lower_bounds, upper_bounds  = baseCuadraticFuncArgs()
        # Call curvi with a less strict epsilon
        epsilon_permissive = 0.1
        x_opt_permissive,f_opt_permissive = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon_permissive)
        # Call curvi with a MORE strict epsilon
        epsilon_strict = 0.00001
        x_opt_strict,f_opt_strict = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon_strict)
        # Compare X distances to correct answer
        x_distance_permissive = abs(x_opt_permissive[0])
        x_distance_strict = abs(x_opt_strict[0])
        if x_distance_permissive < x_distance_strict:
            error_msg = "The strict X should be closer to the correct value than the permissive. " \
                        "X_permissive: {0}. X_strict: {1}".format(x_opt_permissive[0], x_opt_strict[0])
            self.fail(error_msg)
        # Compare f(x) distances to correct answer
        f_distance_permissive = abs(f_opt_permissive)
        f_distance_strict = abs(f_opt_strict)
        if f_distance_permissive < f_distance_strict:
            error_msg = "The strict f(x) should be closer to the correct value than the permissive. " \
                        "X_permissive: {0}. X_strict: {1}".format(f_opt_permissive, f_opt_strict)
            self.fail(error_msg)

    def test_curvi_x0_of_size_larger_than_one(self):
        curvi_mod = self.tryToImportCurviModule()
        # Get base args for an example function
        x0, obj_func, epsilon, lower_bounds, upper_bounds  = baseCuadraticFuncArgsForVectorOf4()
        # Call curvi
        x_opt,f_opt = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon)
        # Check results
        correct_x_opt = [0, 0, 0, 0]
        x_distance_to_origin = sum([x_opt[i] - correct_x_opt[i] for i in range(4)])
        if not numpy.isclose(x_distance_to_origin,0,atol=epsilon):
            error_msg = "x_opt distance should be close to {0}" \
                        " but instead it is {1}".format(0,x_distance_to_origin)
            self.fail(error_msg)
        correct_f_opt = 0
        if not numpy.isclose(f_opt,correct_f_opt, atol=epsilon):
            error_msg = "f_opt should be close to {0} but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)

    def test_curvi_max_instead_of_min(self):
        curvi_mod = self.tryToImportCurviModule()
        # Get base args for an example function
        x0, obj_func, epsilon, lower_bounds, upper_bounds  = baseCuadraticFuncArgs()
        # Replace objective function to maximize instead of minimizing
        obj_func = lambda x: -x**2
        # Call curvi
        x_opt,f_opt = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon)
        # Check results
        correct_x_opt_abs = [2]
        if not numpy.isclose(abs(x_opt),correct_x_opt_abs):
            error_msg = "abs(x_opt) should be close to {0} but instead it is {1}".format(correct_x_opt_abs,abs(x_opt))
            self.fail(error_msg)
        correct_f_opt = -4
        if not numpy.isclose(f_opt,correct_f_opt):
            error_msg = "f_opt should be close to {0} but instead it is {1}".format(correct_f_opt,f_opt)
            self.fail(error_msg)

    def test_curvi_irrelevant_dimension(self):
        curvi_mod = self.tryToImportCurviModule()
        # Define a function that ignores one of the dimensions
        x0 = numpy.array([1,43])
        obj_func = lambda x: x[0]**2
        epsilon = 0.0001
        lower_bounds = [-2,-100]
        upper_bounds = [2,100]
        # Call curvi
        x_opt,f_opt = curvi_mod.curvif_simplified(x0,obj_func,lower_bounds,upper_bounds,epsilon)
        # Check results
        correct_x_opt_first = 0
        x_opt_first = x_opt[0]
        if not numpy.isclose(x_opt_first,correct_x_opt_first):
            error_msg = "x_opt[0] should be close to {0} but instead it is {1}".format(correct_x_opt_first,x_opt_first)
            self.fail(error_msg)
        correct_f_opt = 0
        if not numpy.isclose(f_opt,correct_f_opt):
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


def baseCuadraticFuncArgs():
    x0 = numpy.array([1])
    obj_func = lambda x: x**2
    epsilon = 0.0001
    lower_bounds = [-2]
    upper_bounds = [2]
    return x0, obj_func, epsilon, lower_bounds, upper_bounds

def baseCuadraticFuncArgsForVectorOf4():
    x0 = numpy.array([1,-1,2,-2])
    obj_func = lambda x: sum([x_i**2 for x_i in x])
    epsilon = 0.0001
    lower_bounds = 4*[-2]
    upper_bounds = 4*[2]
    return x0, obj_func, epsilon, lower_bounds, upper_bounds
