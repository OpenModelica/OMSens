#Std
import unittest
import os
import tempfile #para crear el tempdir
import shutil #para borrar el tempdir
import re #para los regex
#Mine
import tests.aux_tests
import running.run_omc as omc_runner

class TestsCompareTwoCSVs(unittest.TestCase):
#setup y teardown de los tests
    def setUp(self):
        #Create tempdir and save its path
        self._temp_dir = tempfile.mkdtemp()
        self._temp_files = [] #each test case can create individual files
    def tearDown(self):
        pass
        shutil.rmtree(self._temp_dir)
        for f in self._temp_files:
            f.close()
#TDD
    # def test_empty_csv_raises_exception(self):
    #     file_path= os.path.join(currentdir, csvs_path+"/empty_file.csv")
    #     self.assertRaises(EmptyCSVException,CSVData,file_path)
    def test_omc_loads_a_model_correctly(self):
        mos_str= model_str
        mos_path=createTMPMos(mos_str,self)
        process_output = omc_runner.runMosScript(mos_path)
        self.assertEqual(process_output,"true\n")

    def test_omc_builds_a_model_correctly(self):
        mos_str= model_str + build_model_str
        mos_path=createTMPMos(mos_str,self)
        process_output = omc_runner.runMosScript(mos_path)
        error_line = process_output.splitlines()[-1]
        self.assertEqual(error_line,'""')
        # The following should be another test but beacuse of slow building times, we minimize the
        # amount of compiling Modelica times
        # test_omc_leaves_no_trash_after_building(self):
        mos_folder_path=os.path.dirname(mos_path)
        trash_files = []
        for x in os.listdir(mos_folder_path):
            if re.match('.*\.(c|o|h|makefile|log|libs|json)$', x):
                trash_files.append(x)
        self.assertEqual(trash_files,[])

        #BORRA DE ACA PARA ABAJO:
        # print(mos_folder_path)
        # print(os.listdir(mos_folder_path))
        # with open(mos_path,"r") as outf:
        #     print(outf.read())
        # print(process_output)
        # self.assertTrue(False)

###########
# Globals #
###########
def createTMPMos(file_str,test_case):
    # Creates mos script in temp folder
    return tests.aux_tests.createTempFromStrIntoTestCaseTempFolder(file_str,test_case,suffix=".mos")
    # Creates stand alone tempfile
    # return tests.aux_tests.createTempFromStrAndAddToTestCase(file_str,test_case,suffix=".mos")
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
