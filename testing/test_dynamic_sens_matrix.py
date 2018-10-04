#Std
import unittest
import os
import tempfile #para crear el tempdir
import shutil #para borrar el tempdir
import re #para los regex
#Mine
import testing.aux_tests
import filesystem.files_aux
import misc.csv_output_to_csv_matrix_converter as to_matrix

class TestsW3SensToMatrixInputOutput(unittest.TestCase):
#setup y teardown de los tests
    def setUp(self):
        #Create tempdir and save its path
        self._temp_dir = tempfile.mkdtemp()
        self._temp_files = [] #each test case can create individual files
        pass
    def tearDown(self):
        shutil.rmtree(self._temp_dir)
        for f in self._temp_files:
            f.close()
        pass
#TDD
    def test_empty_csvstring_raises_exception(self):
        ### NEEDS WRITING!
        self.assertTrue(True)
        # csvstring = EMPTY_CSVSTR
        # self.assertRaises(EmptyCSVException,CSVData,file_path)

class TestsW3TheoSensToMatrixProccessing(unittest.TestCase):
    def test_one_param_one_var_one_year(self):
        w3TheoSens_str = w3TheoSens_oneParamOneVarOneYear_str
        rows_str_list = to_matrix.W3TheoSensToMatrixRowsListFromYear(w3TheoSens_str,1901)
        # Assert that the header row has the correct variable name
        self.assertEqual(rows_str_list[0].split(",")[1],"Arable_Land_Dynamics1.Arable_Land.Integrator1.y")
        # Assert that the value row has the correct param and value
        self.assertEqual(rows_str_list[1].split(",")[0],"agr_inp_init")
        self.assertEqual(rows_str_list[1].split(",")[1],"43")

    def test_one_param_one_var_5_years(self):
        w3TheoSens_str = w3TheoSens_oneParamOneVar5Years_str
        rows_str_list = to_matrix.W3TheoSensToMatrixRowsListFromYear(w3TheoSens_str,1903)
        # Assert that the header row has the correct variable name
        self.assertEqual(rows_str_list[0].split(",")[1],"Arable_Land_Dynamics1.Arable_Land.Integrator1.y")
        # Assert that the value row has the correct param and value
        self.assertEqual(rows_str_list[1].split(",")[0],"agr_inp_init")
        self.assertEqual(rows_str_list[1].split(",")[1],"33")

    def test_one_param_one_var_one_year_3_values(self):
        w3TheoSens_str = w3TheoSens_oneParamOneVarOneYear2Values_str
        self.assertRaises(to_matrix.InvalidW3TheoSensCSVException,to_matrix.W3TheoSensToMatrixRowsListFromYear,w3TheoSens_str,1901)

    def test_one_param_2_vars_one_year_1_value(self):
        w3TheoSens_str = w3TheoSens_oneParam2VarsOneYearOneValue_str
        self.assertRaises(to_matrix.InvalidW3TheoSensCSVException,to_matrix.W3TheoSensToMatrixRowsListFromYear,w3TheoSens_str,1901)

    def test_2_params_2_vars_one_year_but_repeated_param_and_var(self):
        w3TheoSens_str = w3TheoSens_2Params2VarsOneYearButRepeatedParamAndVar_str
        self.assertRaises(to_matrix.RepeatedParamVarPairException,to_matrix.W3TheoSensToMatrixRowsListFromYear,w3TheoSens_str,1901)

    def test_2_params_3_vars_one_year(self):
        w3TheoSens_str = w3TheoSens_2Params3VarsOneYear_str
        self.assertRaises(to_matrix.DifferentInfluencedVariablesException,to_matrix.W3TheoSensToMatrixRowsListFromYear,w3TheoSens_str,1901)

    def test_one_param_one_var_one_year_but_invalid_year(self):
        w3TheoSens_str = w3TheoSens_oneParamOneVarOneYear_str
        self.assertRaises(to_matrix.InvalidYearException,to_matrix.W3TheoSensToMatrixRowsListFromYear,w3TheoSens_str,1902)

###########
# Globals #
###########
w3TheoSens_oneParamOneVarOneYear_str = \
"""time,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y
1901,43"""

w3TheoSens_oneParamOneVar5Years_str = \
"""time,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y
1901,43
1902,23
1903,33
1904,53
1905,63"""

w3TheoSens_oneParamOneVarOneYear2Values_str = \
"""time,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y
1901,43,44"""

w3TheoSens_oneParam2VarsOneYearOneValue_str = \
"""time,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator2.y
1901,43"""
w3TheoSens_2Params2VarsOneYearButRepeatedParamAndVar_str = \
"""time,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y
1901,43,33"""

w3TheoSens_2Params3VarsOneYear_str = \
"""time,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y,$Sensitivities.agr_inp_init_2.Arable_Land_Dynamics1.Arable_Land.Integrator1.y,$Sensitivities.agr_inp_init_2.Arable_Land_Dynamics1.Arable_Land.Integrator2.y
1901,43,33,53"""
