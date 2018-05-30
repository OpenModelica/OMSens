#Std
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
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
            "perturbed_simus_info"               :
                {
                    "e":
                        {
                            "simu_file_path": StringIO(bb_e_perturbed_str),
                            "std_val"       : 0.7,
                            "perturbed_val" : 0.735,
                        },
                    "g":
                        {
                            "simu_file_path": StringIO(bb_g_perturbed_str),
                            "std_val"       : 9.81,
                            "perturbed_val" : 10.3005,
                        }
                },
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
        vars_sens_info = analysis_files_paths["vars_sens_info"]
        params_strs = ["e","g"]
        # Method results for the run being tested:
        g_rel_method_per_var = {
            "h": [ "251928", "001858"],
        }
        # Test sens info files
        # Iterate the results testing that they include the necessary information
        # Run info csvs:
        for t_var in analyze_csvs_kwargs["target_vars"]:
            # Read file into memory as str
            run_info_path = vars_sens_info[t_var]
            run_info_str  = filesystem.files_aux.readStrFromFile(run_info_path)
            # Get the list of strings that the file must include
            strs_to_include = params_strs + g_rel_method_per_var[t_var]
            # Check that the strs are included
            for s in strs_to_include:
                if s not in run_info_str:
                    self.fail("The sens info file should but doesn't include the string {0}.".format(s))
        # Test sens matrices files
        methods_correct_vals_tuples = [("rel", "251928"), ("rms", "04251")]
        sens_mats_paths_dict = analysis_files_paths["sens_matrices"]
        for method_name, str_to_include in methods_correct_vals_tuples:
            # Get path for this method's matrix
            mat_path = sens_mats_paths_dict[method_name]
            # Read file into memory as str
            mat_str = filesystem.files_aux.readStrFromFile(mat_path)
            # Check that the strs are included
            if str_to_include not in mat_str:
                self.fail("The matrix file should but doesn't include the string {0}.".format(str_to_include))



    def test_different_shapes_raises_error(self):
        # For RMS we need all of the simulation results (std run and perturbed runs) to have the same amount of rows.
        # First sub-test: e has 1 more row
        analyze_csvs_kwargs_1 = {
            "perturbed_simus_info"               :
                {
                    "e":
                        {
                            "simu_file_path": StringIO(bb_e_perturbed_2_str),
                            "std_val"       : 0.7,
                            "perturbed_val" : 0.735,
                        },
                    "g":
                        {
                            "simu_file_path": StringIO(bb_g_perturbed_str),
                            "std_val"       : 9.81,
                            "perturbed_val" : 10.3005,
                        }
                },
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
            "perturbed_simus_info"               :
                {
                    "e":
                        {
                            "simu_file_path": StringIO(bb_e_perturbed_str),
                            "std_val"       : 0.7,
                            "perturbed_val" : 0.735,
                        },
                    "g":
                        {
                            "simu_file_path": StringIO(bb_g_perturbed_2_str),
                            "std_val"       : 9.81,
                            "perturbed_val" : 10.3005,
                        }
                },
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
            "perturbed_simus_info"               :
                {
                    "e":
                        {
                            "simu_file_path": StringIO(bb_e_perturbed_str),
                            "std_val"       : 0.7,
                            "perturbed_val" : 0.735,
                        },
                    "g":
                        {
                            "simu_file_path": StringIO(bb_g_perturbed_2_str),
                            "std_val"       : 9.81,
                            "perturbed_val" : 10.3005,
                        }
                },
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
