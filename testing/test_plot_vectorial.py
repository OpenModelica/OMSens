# Std
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
import os
import re
import pandas
from io import StringIO

# Mine
from plotting.plot_vectorial import VectorialPlotter
import vectorial.optimization_result as optimization_result_f




class TestVectorialPlot(unittest.TestCase):
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
    def test_plot_vectorial_creates_files_in_folder(self):
#        # Write CSV strs to file
#        x0_run_csv_path = os.path.join(self._temp_dir, "x0_run.csv")
#        files_aux.writeStrToFile(x0_run_str, x0_run_csv_path)
#        x_opt_run_csv_path = os.path.join(self._temp_dir, "x_opt_run.csv")
#        files_aux.writeStrToFile(x_opt_run_str, x_opt_run_csv_path)
#        # Read df from strs
#        df_x0_run = pandas.read_csv(x0_run_csv_path, index_col=0)
#        df_x_opt_run = pandas.read_csv(x_opt_run_csv_path, index_col=0)

        # Read df from strs
        df_x0_run = pandas.read_csv(StringIO(x0_run_str), index_col=0)
        df_x_opt_run = pandas.read_csv(StringIO(x_opt_run_str), index_col=0)
        # Create an example vectorial
        optim_res = self.optimizationResultsExample()
        # Initialize vectorial plotter
        vectorial_plotter = VectorialPlotter(optim_res, df_x0_run, df_x_opt_run)
        # Plot vectorial specs to temp folder
        vectorial_plotter.plotInFolder(self._temp_dir)
        # Get plots extensions regex
        regex = '.*\.(png|svg)$'
        # Get list of files from regex
        files_in_dir = os.listdir(self._temp_dir)
        plot_files = [x for x in files_in_dir if re.match(regex, x)]
        # Check that there is at least one plot
        if len(plot_files) < 1:
            error_msg = "The plot function should create at least one plot file in the destination folder."
            self.fail(error_msg)


    # Auxs:
    def optimizationResultsExample(self):
        # Optimization results info
        optim_res = optimization_result_f.ModelOptimizationResult(
            x0 =  {
              "realParam1": 1.121,
              "realParam2": 1.122,
              "realParam3": 1.123
            },
            x_opt = {
              "realParam1": 1.0649500000000849,
              "realParam2": 1.1220002551794537,
              "realParam3": 1.1363476851600545
            },
            f_x_opt       = 322.6798500000257,
            f_x0          = 339.663,
            stop_time     = 3,
            variable_name = "outvar1",
        )
        return optim_res

###########
# Globals #
###########
model_str = \
"""model ModelWithVariousParams
  // Params
  parameter Real    realParam1 = 1.121;
  parameter Real    realParam2 = 1.122;
  parameter Real    realParam3 = 1.123;
  parameter Integer intParam1  = 101;
  parameter Integer intParam2  = 102;
  parameter Integer intParam3  = 103;

  // Vars
  output Real outvar1;
  output Real outvar2;
  output Real outvar3;
equation
  outvar1 = time * realParam1 * intParam1;
  outvar2 = time * realParam2 * intParam2;
  outvar3 = time * realParam3 * intParam3;
end ModelWithVariousParams;"""

x0_run_str = \
""""time","outvar1","outvar2","outvar3"
0,0,0,0
0.1,11.3221,11.4444,11.5669
0.2,22.6442,22.8888,23.1338
0.3,33.9663,34.33320000000001,34.7007
0.4,45.2884,45.77760000000001,46.2676
0.5,56.6105,57.22200000000001,57.8345
0.6,67.93259999999999,68.66640000000001,69.4014
0.7,79.2547,80.11080000000001,80.9683
0.8,90.57680000000001,91.55520000000001,92.5352
0.9,101.8989,102.9996,104.1021
1,113.221,114.444,115.669
1.1,124.5431,125.8884,127.2359
1.2,135.8652,137.3328,138.8028
1.3,147.1873,148.7772,150.3697
1.4,158.5094,160.2216,161.9366
1.5,169.8315,171.666,173.5035
1.6,181.1536,183.1104,185.0704
1.7,192.4757,194.5548,196.6373
1.8,203.7978,205.9992,208.2042
1.9,215.1199,217.4436,219.7711
2,226.442,228.888,231.338
2.1,237.7641,240.3324,242.9049
2.2,249.0862,251.7768000000001,254.4718
2.3,260.4083,263.2212,266.0386999999999
2.4,271.7304,274.6656,277.6056
2.5,283.0525,286.11,289.1725
2.6,294.3746,297.5544,300.7394
2.7,305.6967,308.9988000000001,312.3063
2.8,317.0188,320.4432,323.8732
2.9,328.3409,331.8876,335.4401
3,339.663,343.3320000000001,347.007"""

x_opt_run_str = \
"""time","outvar1","outvar2","outvar3"
0,0,0,0
0.1,10.75599500000086,11.44440260283043,11.70438115714856
0.2,21.51199000000172,22.88880520566086,23.40876231429712
0.3,32.26798500000257,34.33320780849128,35.11314347144568
0.4,43.02398000000343,45.77761041132172,46.81752462859424
0.5,53.77997500000428,57.22201301415214,58.5219057857428
0.6,64.53597000000514,68.66641561698256,70.22628694289136
0.7,75.29196500000599,80.11081821981298,81.93066810003992
0.8,86.04796000000687,91.55522082264343,93.63504925718848
0.9,96.80395500000772,102.9996234254739,105.339430414337
1,107.5599500000086,114.4440260283043,117.0438115714856
1.1,118.3159450000094,125.8884286311347,128.7481927286342
1.2,129.0719400000103,137.3328312339651,140.4525738857827
1.3,139.8279350000111,148.7772338367956,152.1569550429313
1.4,150.583930000012,160.221636439626,163.8613362000798
1.5,161.3399250000128,171.6660390424564,175.5657173572284
1.6,172.0959200000137,183.1104416452869,187.270098514377
1.7,182.8519150000146,194.5548442481173,198.9744796715255
1.8,193.6079100000154,205.9992468509477,210.6788608286741
1.9,204.3639050000163,217.4436494537781,222.3832419858227
2,215.1199000000171,228.8880520566086,234.0876231429712
2.1,225.875895000018,240.332454659439,245.7920043001198
2.2,236.6318900000189,251.7768572622694,257.4963854572683
2.3,247.3878850000197,263.2212598650998,269.2007666144169
2.4,258.1438800000205,274.6656624679302,280.9051477715655
2.5,268.8998750000214,286.1100650707607,292.609528928714
2.6,279.6558700000223,297.5544676735911,304.3139100858626
2.7,290.4118650000232,308.9988702764216,316.0182912430112
2.8,301.1678600000239,320.4432728792519,327.7226724001597
2.9,311.9238550000248,331.8876754820824,339.4270535573082
3,322.6798500000257,343.3320780849128,351.1314347144568"""
