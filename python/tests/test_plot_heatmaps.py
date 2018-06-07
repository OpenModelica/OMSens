# Std
import shutil  # para borrar el tempdir
import tempfile  # para crear el tempdir
import unittest
from io import StringIO

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
    def test_heatmap_is_created_correctly_from_good_matrix(self):
        # Plot heatmap from matrix as pandas DF
        plot_heatmap.plotHeatmapFromMatrixAsDataFrame(good_df_matrix)


# Test examples
good_df_matrix = \
    """param\ var,var_1,var_2_var_3
    param_1,1,2,3
    param_2,4,5,6
    param_3,7,8,9"""
