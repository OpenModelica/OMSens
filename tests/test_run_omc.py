#Std
import unittest
import os
import tempfile #para crear el tempdir
import shutil #para borrar el tempdir
import re #para los regex
#Mine
import tests.aux_tests
import running.run_omc as omc_runner
import filesystem.files_aux

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

    def test_sensitivity_analysis_enabled_creates_new_meta_vars(self):
        # Again, more than one test in one to minimize building times
        # Test: omc builds with sensitivity flags without errors
        mos_str= model_str + command_line_sensitivity_flag_str + build_model_sensitivity_str
        mos_path=createTMPMos(mos_str,self)
        process_output = omc_runner.runMosScript(mos_path)
        error_line = process_output.splitlines()[-1]
        self.assertEqual(error_line,'""')
        # Test: running the executable binary creates a .mat with new meta vars
        mos_folder_path=os.path.dirname(mos_path)
        trash_files = []
        for x in os.listdir(mos_folder_path):
            if re.match('.*\.(c|o|h|makefile|log|libs|json)$', x):
                trash_files.append(x)
        cmd = cmd_sensitivity_to_run_str
        exe_call_output = filesystem.files_aux.callCMDStringInPath(cmd,mos_folder_path)
        mat_grep_cmd = """strings archivito.mat | grep "\$Sens" """


        for x in os.listdir(mos_folder_path):
            print(x)
        self.assertEqual(trash_files,[])
        #DELETE FROM HERE DOWN:
        # print(mos_folder_path)
        # print(os.listdir(mos_folder_path))
        # with open(mos_path,"r") as outf:
        #     print(outf.read())
        # print(process_output)
        self.assertTrue(False)
        #DELETE UNTIL HERE ^

###########
# Globals #
###########
def createTMPMos(file_str,test_case):
    # Creates mos script in temp folder
    return tests.aux_tests.createTempFromStrIntoTestCaseTempFolder(file_str,test_case,"script.mos")
    # Creates stand alone tempfile
    # return tests.aux_tests.createTempFromStrAndAddToTestCase(file_str,test_case,suffix=".mos")
model_str =\
"""loadString("
class Model
  parameter Real a=-1;
  Real x(start=1,fixed=true);
equation
  der(x) = a*x;
end Model;
");\n """
build_model_str =\
"""buildModel(Model);getErrorString();\n"""
build_model_sensitivity_str=\
"""buildModel(Model, method="ida");getErrorString();\n"""
set_initial_val_str =\
"""setInitXmlStartValue("Model_init.xml", "x", String(1) , "Model_init.xml");"""
command_line_sensitivity_flag_str=\
"""setCommandLineOptions("+calculateSensitivities"); getErrorString();\n"""
cmd_sensitivity_to_run_str=\
"""./Model -idaSensitivity -r=archivito.mat;\n"""
#
#
#
# loadModel(Modelica); getErrorString();
#
# print("*** Loading SystemDynamics...");
# //loadFile("/home/adanos/Documents/TPs/tesis/repos/modelica_scripts/resource/SystemDynamics/package.mo");
# //loadFile("/home/adanos/Documents/modelica/scripts/scriptBernhard/SystemDynamics/package.mo");
# loadFile("/home/adanos/Documents/modelica/sys_dyn/SystemDynamics/package.mo");
#
#
# print("*** Moving to ./temp");
# cd("temp"); getErrorString();
#
# print("*** Building");
# setCommandLineOptions("+calculateSensitivities"); getErrorString();
# buildModel(SystemDynamics.WorldDynamics.World3.Scenario_1, method="ida");
# for i in 0:8 loop
#   value := i*1;
#   stopTime := 1993 + value;
#   sed_cmd := "sed -i 's/^ *stopTime *=.*$/   stopTime = \""+String(stopTime)+"\"/g' SystemDynamics.WorldDynamics.World3.Scenario_1_init.xml";
# //  print(sed_cmd+"\n");
#   system(sed_cmd);
#   print("*** Changed stopTime to: "+String(stopTime)+"\n");
#   file_name_i :=  "w3_stopTime_" + String(stopTime) + ".mat";
#   cmd := "./SystemDynamics.WorldDynamics.World3.Scenario_1  -idaSensitivity "+ "-r="+file_name_i;//+")";
#   print("Running command: "+cmd+"\n");
#   print("Date & time beggining: ");
#   system("date"); print("\n");
#   system(cmd);
#   print("Date & time end:       ");
#   system("date"); print("\n");
#   getErrorString();
#   //plot(plot_var,fileName=file_name_i,externalWindow=true);
# end for;
#
#         mos_path=createTMPMos(mos_str,self)
#         process_output = omc_runner.runMosScript(mos_path)
#         error_line = process_output.splitlines()[-1]
#         self.assertEqual(error_line,'""')
#
#         mos_folder_path=os.path.dirname(mos_path)
#         trash_files = []
#         for x in os.listdir(mos_folder_path):
#             if re.match('.*\.(c|o|h|makefile|log|libs|json)$', x):
#                 trash_files.append(x)
#         self.assertEqual(trash_files,[])
#         #BORRA DE ACA PARA ABAJO:
#         # print(mos_folder_path)
#         # print(os.listdir(mos_folder_path))
#         # with open(mos_path,"r") as outf:
#         #     print(outf.read())
#         # print(process_output)
#         # self.assertTrue(False)
#
# ###########
# # Globals #
# ###########
# def createTMPMos(file_str,test_case):
#     # Creates mos script in temp folder
#     return tests.aux_tests.createTempFromStrIntoTestCaseTempFolder(file_str,test_case,"script.mos")
#     # Creates stand alone tempfile
#     # return tests.aux_tests.createTempFromStrAndAddToTestCase(file_str,test_case,suffix=".mos")
# model_str =\
# """loadString("
# class Model
#   parameter Real a=-1;
#   Real x(start=1,fixed=true);
# equation
#   der(x) = a*x;
# end Model;
# ");\n """
# build_model_str =\
# """buildModel(Model);getErrorString();\n"""
# set_initial_val_str =\
# """setInitXmlStartValue("Model_init.xml", "x", String(1) , "Model_init.xml");"""
#
#
#
#
#
#
#
#
#
#
#
#
#
# i
#
#
#
#
#
#
#
#
#
#
# i
