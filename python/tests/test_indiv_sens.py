#Std
import unittest
import os
import tempfile #para crear el tempdir
import shutil #para borrar el tempdir
import re #para los regex
from io import StringIO
# Mine
import analysis.indiv_sens
import filesystem.files_aux

class TestIndividualSensitivityAnalysis(unittest.TestCase):
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
# Tests:
    def test_sens_run_gives_correct_results(self):
        # Run info. This corresponds to a simulation that perturbed some parameters in isolation. To avoid running the simulation in this test,
        #   we save the simulation's result instead.
        analyze_csvs_kwargs = {
            "perturbed_csvs_path_and_info_pairs" : [(StringIO(bb_e_perturbed_str), ('e', 0.7, 0.735)), (StringIO(bb_g_perturbed_str), ('g', 9.81, 10.3005))],
            "std_run_csv_path"                   : StringIO(bb_std_run_str),
            "target_vars"                        : ['h'],
            "percentage_perturbed"               : 5,
            "specific_year"                      : 3,
            "output_folder_analyses_path"        : self._temp_dir,
            "rms_first_year"                     : 0,
            "rms_last_year"                      : 3,
        }
        # Run analysis from simulation info
        analysis_files_paths = analysis.indiv_sens.completeIndividualSensAnalysis(**analyze_csvs_kwargs)
        # Test that that the resulting run info includes the basic info: all param names, default and perturbed vals, the variable and its value
        run_infos_per_var = analysis_files_paths["run_infos_per_var"]
        params_strs = [str(x) for param_info_tuple in analyze_csvs_kwargs["perturbed_csvs_path_and_info_pairs"] for x in param_info_tuple[1]]
        # Method results for the run being tested:
        g_rel_method_per_var = {
            "h": [ "251928", "001858"],
        }
        # Iterate the results testing that they include the necessary information
        # Run info csvs:
        for t_var in analyze_csvs_kwargs["target_vars"]:
            # Read file into memory as str
            run_info_path = run_infos_per_var[t_var]
            run_info_str  = filesystem.files_aux.readStrFromFile(run_info_path)
            # Get the list of strings that the file must include
            strs_to_include = params_strs + g_rel_method_per_var[t_var]
            # Check that the strs are included
            for s in strs_to_include:
                if s not in run_info_str:
                    self.fail("The file should but doesn't include the string {0}.".format(s))

    def test_different_shapes_raises_error(self):
        # For RMS we need all of the simulation results (std run and perturbed runs) to have the same amount of rows.
        # First sub-test: e has 1 more row
        analyze_csvs_kwargs_1 = {
            "perturbed_csvs_path_and_info_pairs" : [(StringIO(bb_e_perturbed_2_str), ('e', 0.7, 0.735)), (StringIO(bb_g_perturbed_str), ('g', 9.81, 10.3005))],
            "std_run_csv_path"                   : StringIO(bb_std_run_str),
            "target_vars"                        : ['h'],
            "percentage_perturbed"               : 5,
            "specific_year"                      : 3,
            "output_folder_analyses_path"        : self._temp_dir,
            "rms_first_year"                     : 0,
            "rms_last_year"                      : 3,
        }
        # Second sub-test: g has 1 more row
        analyze_csvs_kwargs_2 = {
            "perturbed_csvs_path_and_info_pairs" : [(StringIO(bb_e_perturbed_str), ('e', 0.7, 0.735)), (StringIO(bb_g_perturbed_2_str), ('g', 9.81, 10.3005))],
            "std_run_csv_path"                   : StringIO(bb_std_run_str),
            "target_vars"                        : ['h'],
            "percentage_perturbed"               : 5,
            "specific_year"                      : 3,
            "output_folder_analyses_path"        : self._temp_dir,
            "rms_first_year"                     : 0,
            "rms_last_year"                      : 3,
        }
        # Third sub-test: std has 1 more row
        analyze_csvs_kwargs_3 = {
            "perturbed_csvs_path_and_info_pairs" : [(StringIO(bb_e_perturbed_str), ('e', 0.7, 0.735)), (StringIO(bb_g_perturbed_str), ('g', 9.81, 10.3005))],
            "std_run_csv_path"                   : StringIO(bb_std_run_2_str),
            "target_vars"                        : ['h'],
            "percentage_perturbed"               : 5,
            "specific_year"                      : 3,
            "output_folder_analyses_path"        : self._temp_dir,
            "rms_first_year"                     : 0,
            "rms_last_year"                      : 3,
        }
        # Run with the 3 kwargs and assert that all of them raise an exception
        self.assertRaises(analysis.indiv_sens.InvalidSimulationResultsException,analysis.indiv_sens.completeIndividualSensAnalysis,**analyze_csvs_kwargs_1)
        self.assertRaises(analysis.indiv_sens.InvalidSimulationResultsException,analysis.indiv_sens.completeIndividualSensAnalysis,**analyze_csvs_kwargs_2)
        self.assertRaises(analysis.indiv_sens.InvalidSimulationResultsException,analysis.indiv_sens.completeIndividualSensAnalysis,**analyze_csvs_kwargs_3)



###########
# Globals #
###########
bb_std_run_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.2250597607429705,-2.279940238910565,-2.279940238910565,-9.81,3.100612842801532,1,0
2,0.04243354772647411,-0.5463586255141026,-0.5463586255141026,-9.81,1.063510205007515,1,0
3,2.101988323055078e-11,0,0,0,0,0,1"""

bb_e_perturbed_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.3100904028764322,-2.124909596770488,-2.124909596770488,-9.81,3.255643484941609,1,0
2,0.04233293611696021,0.9167931152103947,0.9167931152103947,-9.81,1.292703301139997,1,0
3,2.631538447381662e-11,0,0,0,0,0,1"""

bb_g_perturbed_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-10.3005,0,1,0
1,0.1657651633154364,-2.584484836337927,-2.584484836337927,-10.3005,3.177182714449088,1,0
2,0.003483617140901725,-1.056333590801138,-1.056333590801138,-10.3005,1.089773670982276,1,0
3,2.105894579818758e-11,0,0,0,0,0,1"""

bb_std_run_2_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.2250597607429705,-2.279940238910565,-2.279940238910565,-9.81,3.100612842801532,1,0
2,0.04243354772647411,-0.5463586255141026,-0.5463586255141026,-9.81,1.063510205007515,1,0
2.5,0.14243354772647411,-0.5463586255141026,-0.5463586255141026,-9.81,1.063510205007515,1,0
3,2.101988323055078e-11,0,0,0,0,0,1"""

bb_e_perturbed_2_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-9.81,0,1,0
1,0.3100904028764322,-2.124909596770488,-2.124909596770488,-9.81,3.255643484941609,1,0
2,0.04233293611696021,0.9167931152103947,0.9167931152103947,-9.81,1.292703301139997,1,0
2.5,0.14233293611696021,0.9167931152103947,0.9167931152103947,-9.81,1.292703301139997,1,0
3,2.631538447381662e-11,0,0,0,0,0,1"""

bb_g_perturbed_2_str = \
""""time","h","v","der(h)","der(v)","v_new","flying","impact"
0,1,0,0,-10.3005,0,1,0
1,0.1657651633154364,-2.584484836337927,-2.584484836337927,-10.3005,3.177182714449088,1,0
2,0.003483617140901725,-1.056333590801138,-1.056333590801138,-10.3005,1.089773670982276,1,0
2.5,0.103483617140901725,-1.056333590801138,-1.056333590801138,-10.3005,1.089773670982276,1,0
3,2.105894579818758e-11,0,0,0,0,0,1"""
