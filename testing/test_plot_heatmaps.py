# For tests
import io
import os
import re
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest

# Std
import pandas

# Mine
from plotting import plot_heatmap as plot_heatmap


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
        # Get dataframe from test data
        df_path = io.StringIO(good_df_matrix)
        df = pandas.read_csv(df_path, index_col=0)
        # Initialize heatmap
        heatmap = plot_heatmap.Heatmap(df)
        # Get the dataframe that will be used for heatmap creation
        df_manipulated = heatmap.heatmapDataFrame()
        # Check that the index (parameters) are sorted in the correct order
        df_manipulated_indices = list(df_manipulated.index)
        correct_params_indices = ["param_3", "param_2", "param_1"]
        for heatmap_param, correct_param in zip(df_manipulated_indices, correct_params_indices):
            if heatmap_param != correct_param:
                error_msg = "The heatmap should have the following params order:\n {0}\n but instead it has the " \
                            "following:\n {1}".format(correct_params_indices,df_manipulated_indices)
                self.fail(error_msg)

    def test_heatmap_has_columns_sorted(self):
        """ Test that the DF matrix has the variables sorted by some criteria. For example, alphabetical order. """
        # Get dataframe from test data
        df_path = io.StringIO(good_df_matrix)
        df = pandas.read_csv(df_path,index_col=0)
        # Initialize heatmap
        heatmap = plot_heatmap.Heatmap(df)
        # Get the dataframe that will be used for heatmap creation
        df_manipulated = heatmap.heatmapDataFrame()
        # Check that the index (parameters) are sorted in the correct order
        df_manipulated_cols = df_manipulated.columns.values.tolist()
        correct_params_cols = ["var_1","var_2","var_3"]
        for heatmap_var,correct_var in zip(df_manipulated_cols,correct_params_cols):
            if heatmap_var != correct_var:
                error_msg = "The heatmap should have the following vars order:\n {0}\n but instead it has the " \
                            "following:\n {1}".format(correct_params_cols,df_manipulated_cols)
                self.fail(error_msg)

    def test_heatmap_plot_creates_files_in_folder(self):
        """ Test that the plot function creates files with plot extensions in the indicated path."""
        # Get dataframe from test data
        df_path = io.StringIO(good_df_matrix)
        df = pandas.read_csv(df_path, index_col=0)
        # Initialize heatmap
        heatmap = plot_heatmap.Heatmap(df)
        # Plot heatmap into temp folder path
        heatmap.plotInFolder(self._temp_dir)
        # Get plots extensions regex
        regex = '.*\.(png|svg)$'
        # Get list of files from regex
        files_in_dir = os.listdir(self._temp_dir)
        plot_files = [x for x in files_in_dir if re.match(regex, x)]
        # Check that there is at least one plot
        if len(plot_files) < 1:
            error_msg = "The plot function should create at least one plot file in the destination folder."
            self.fail(error_msg)

# Test examples
good_df_matrix = \
"""param\ var,var_2,var_3,var_1
param_1,1,2,3
param_2,4,5,6
param_3,7,8,9"""
