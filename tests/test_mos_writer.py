#Std
import unittest
import os
import tempfile #para crear el tempdir
import shutil #para borrar el tempdir
import filecmp #para saber si 2 files son iguales o no
import platform #para saber la platform en la que se está corriendo el script
from nose.plugins.attrib import attr #to tag tests as slow, fast, etc
#Mine
from plotting import plot_csv
import tests.aux_tests
import settings.gral_settings as gral_settings
import filesystem.files_aux

class TestsCompareTwoCSVs(unittest.TestCase):
#setup y teardown de los tests
    def setUp(self):
        #Create tempdir and save its path
        self._temp_dir = tempfile.mkdtemp()
        self._temp_files = [] #each test case can create individual files
    def tearDown(self):
        pass
        # shutil.rmtree(self._temp_dir)
        # for f in self._temp_files:
        #     f.close()
#TDD
    # def test_empty_csv_raises_exception(self):
    #     file_path= os.path.join(currentdir, csvs_path+"/empty_file.csv")
    #     self.assertRaises(EmptyCSVException,CSVData,file_path)
    @attr(speed='fast')
    def test_omc_loads_a_model_correctly(self):
        mos_str= model_str
        mos_path=createTMPMos(mos_str,self)
        process_output = runMosScript(mos_path)
        self.assertEqual(process_output,"true\n")
    @attr(speed='fast')
    def test_omc_builds_a_model_correctly(self):
        mos_str= model_str + build_model_str
        mos_path=createTMPMos(mos_str,self)
        process_output = runMosScript(mos_path)
        error_line = process_output.splitlines()[-1]
        self.assertEqual(error_line,'""')
        # with open(mos_path,"r") as outf:
        #     print(outf.read())
        # print(process_output)
        # self.assertTrue(False)

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
    # else:
        # logger.error("This script was tested only on Windows and Linux. The omc interpreter for another platform has not been set")

    command = "{interpreter} {script_path} +d=initialization".format(interpreter=interpreter,script_path=script_path)
    output = filesystem.files_aux.callCMDStringInPath(command,script_folder_path)
    folder_path = os.path.dirname(script_path)
    omc_log_path = os.path.join(folder_path,gral_settings.omc_run_log_filename)
    output_decoded = output.decode("UTF-8")
    # writeOMCLog(output_decoded,omc_log_path)
    # logger.debug("OMC Log written to: {omc_log_path}".format(omc_log_path=omc_log_path))
    return output_decoded
def createTMPMos(file_str,test_case):
    return tests.aux_tests.createTempFromStrAndAddToTestCase(file_str,test_case,suffix=".mos")
model_str =\
b"""loadString("
class Model
  parameter Real a=-1;
  Real x(start=1,fixed=true);
equation
  der(x) = a*x;
end Model;
");\n """
build_model_str =\
b"""buildModel(Model);getErrorString();\n"""
set_initial_val_str =\
b"""setInitXmlStartValue("Model_init.xml", "x", String(1) , "Model_init.xml");"""
