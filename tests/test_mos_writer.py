#Std
import unittest
import os
import tempfile #para crear el tempdir
import shutil #para borrar el tempdir
import filecmp #para saber si 2 files son iguales o no
from nose.plugins.attrib import attr #to tag tests as slow, fast, etc
#Mine
from plotting import plot_csv
import tests.tests_aux
import settings.gral_settings as gral_settings

class TestsCompareTwoCSVs(unittest.TestCase):
#setup y teardown de los tests
    def setUp(self):
        #Create tempdir and save its path
        self._temp_dir = tempfile.mkdtemp()
        self._temp_files = [] #each test case can create individual files
    def tearDown(self):
        shutil.rmtree(self._temp_dir)
        for f in self._temp_files:
            f.close()
#TDD
    # def test_empty_csv_raises_exception(self):
    #     file_path= os.path.join(currentdir, csvs_path+"/empty_file.csv")
    #     self.assertRaises(EmptyCSVException,CSVData,file_path)
    @attr(speed='fast')
    def test_omc_loads_a_model_correctly(self):
        mo_str= model_str
        mos_path=createTMPMos(model_str(),self)

        # file_1_path = threePoints_sevenVars_csv_path(self)
        # file_2_path = file_1_path
        # output_dir_path = outputDirPath(self)
        # compare_csv_to_orig.compareCSVToOrig(file_1_path,"LA",output_dir_path)
        # # Assert that the final folder has 2 files (book comparison and scan comparison)
        # book_comparison_folder_name = compare_csv_to_orig.bookComparisons_folder_name()
        # scan_comparison_folder_name = compare_csv_to_orig.scanComparisons_folder_name()
        # self.assertEqual(set(os.listdir(output_dir_path)),
        #                  set([book_comparison_folder_name,scan_comparison_folder_name]))

###########
# Globals #
###########
def runMosScript(script_path):
    script_folder_path = os.path.dirname(script_path)
    #Check if windows or linux:
    if platform.system() == "Linux":
        interpreter = gral_settings._interpreter_linux
    elif platform.system() == "Windows":
        interpreter = gral_settings._interpreter_windows
    else:
        logger.error("This script was tested only on Windows and Linux. The omc interpreter for another platform has not been set")

    command = "{interpreter} {script_path}".format(interpreter=interpreter,script_path=script_path)
    output = callCMDStringInPath(command,script_folder_path)
    folder_path = os.path.dirname(script_path)
    omc_log_path = os.path.join(folder_path,gral_settings.omc_run_log_filename)
    output_decoded = output.decode("UTF-8")
    writeOMCLog(output_decoded,omc_log_path)
    logger.debug("OMC Log written to: {omc_log_path}".format(omc_log_path=omc_log_path))
    return output_decoded
def createTMPMos(file_str,test_case):
    return tests.tests_aux.createTempFromContent(file_str,test_case)
def model_str():
    return \
b"""loadString("
class Model
  parameter Real a=-1;
  Real x(start=1);
equation
  der(x) = a*x;
end Model;
"); getErrorString();"""
