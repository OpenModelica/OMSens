# Std
import os
import re  # regex support
import shutil  # tempdir deletion
import tempfile  # tempdir creation
import unittest

import modelica_interface.run_omc as omc_runner
# Mine
import testing.aux_tests


class TestsBuildModel(unittest.TestCase):
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
