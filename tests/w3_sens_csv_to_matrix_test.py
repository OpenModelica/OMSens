#Std
import unittest
import os
import tempfile #para crear el tempdir
import shutil #para borrar el tempdir
import re #para los regex
#Mine
import tests.aux_tests
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
    def test_one_param_one_var(self):
        w3TheoSens_str = w3TheoSens_oneParamOneVar_str
        # DESDE ACA PROBABLEMENTE EN UNA NUEVA FUNCION
        str_lines_list = w3TheoSens_str.split("\n")
        w3theosens_header_row = str_lines_list[0]
        w3theosens_year_row = str_lines_list[1]
        # HASTA ACA PROBABLEMENTE EN UNA NUEVA FUNCION
        rows_str_list = to_matrix.W3TheoSensToMatrixFromHeadersAndYearRow(w3theosens_header_row,w3theosens_year_row)
        # Assert that the header row has the correct variable name
        self.assertEqual(rows_str_list[0].split(",")[1],"Arable_Land_Dynamics1.Arable_Land.Integrator1.y")
        # Assert that the value row has the correct param and value
        self.assertEqual(rows_str_list[1].split(",")[0],"agr_inp_init")
        self.assertEqual(rows_str_list[1].split(",")[1],"43")

###########
# Globals #
###########
w3TheoSens_oneParamOneVar_str = \
"""time,$Sensitivities.agr_inp_init.Arable_Land_Dynamics1.Arable_Land.Integrator1.y
1901,43"""
