# Std
import os
import re  # regex support
import shutil  # tempdir deletion
import tempfile  # tempdir creation
import unittest

import pytest

# Mine
import modelica_interface.run_omc as omc_runner
import testing.aux_tests


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

    # Tests
    def test_omc_loads_a_model_correctly(self):
        mos_str = model_str
        mos_path = createTMPMos(mos_str, self)
        process_output = omc_runner.runMosScript(mos_path)
        self.assertEqual(process_output, "true\n")

    @pytest.mark.slow
    def test_omc_builds_a_model_correctly(self):
        mos_str = model_str + build_model_str
        mos_path = createTMPMos(mos_str, self)
        process_output = omc_runner.runMosScript(mos_path)
        error_line = process_output.splitlines()[-1]
        self.assertEqual(error_line, '""')
        # The following should be another test but because of slow building times, we minimize the
        # amount of compiling Modelica times
        # Test that OMC leaves no trash after building and simulating
        mos_folder_path = os.path.dirname(mos_path)
        trash_files = []
        for x in os.listdir(mos_folder_path):
            if re.match('.*\.(c|o|h|makefile|log|libs|json)$', x):
                trash_files.append(x)
        if len(trash_files) > 0:
            not_removed_files = ",".join(trash_files)
            fail_message = "The following files should've been removed but weren't: {0}".format(not_removed_files)
            self.fail(fail_message)


###########
# Globals #
###########
def createTMPMos(file_str, test_case):
    # Creates mos script in temp folder
    return testing.aux_tests.createTempFromStrIntoTestCaseTempFolder(file_str, test_case, "script.mos")
    # Creates stand alone tempfile
    # return testing.aux_tests.createTempFromStrAndAddToTestCase(file_str,test_case,suffix=".mos")


model_str = \
    """loadString("
    class Model
      parameter Real a=-1;
      Real x(start=1,fixed=true);
    equation
      der(x) = a*x;
    end Model;
    ");\n """

build_model_str = \
    """buildModel(Model);getErrorString();\n"""
