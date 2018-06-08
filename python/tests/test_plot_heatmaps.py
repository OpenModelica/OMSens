# For tests
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
import io

# Std
import pandas

# Mine
import plotting.plot_heatmap as plot_heatmap


class TestPlotHeatmap(unittest.TestCase):
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
    def test_heatmap_has_parameters_sorted(self):
        """ Test that the DF matrix has the parameters sorted by some criteria on the influence on the variables"""
        # Plot heatmap from matrix as pandas DF
        df_path = io.StringIO(good_df_matrix)
        df = pandas.read_csv(df_path,index_col=0)
        # Initialize heatmap
        heatmap = plot_heatmap.Heatmap(df)
        # Ask for the df to be used in the heatmap
        df_manipulated = heatmap.heatmapDataFrame()
        # Check that the index (parameters) are sorted in the correct order
        df_manipulated_index_cols = list(df_manipulated.index)
        correct_params_cols = ["param_3","param_2","param_1"]
        for heatmap_param,correct_param in zip(df_manipulated_index_cols,correct_params_cols):
            if heatmap_param != correct_param:
                error_msg = "The heatmap should have the following params order:\n {0}\n but instead it has the following:\n {1}".format(df_manipulated_index_cols,correct_params_cols)
                self.fail(error_msg)

# Test examples
good_df_matrix = \
"""param\ var,var_1,var_2,var_3
param_1,1,2,3
param_2,4,5,6
param_3,7,8,9"""
