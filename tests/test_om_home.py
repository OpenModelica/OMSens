# Where OMSens looks for OpenModelica: OPENMODELICAHOME, OPENMODELICAHOME_<version>, PATH.
# No omc is started, the installations are directories with an empty bin/omc.exe.
import os
import platform
import shutil
import tempfile
import unittest
from unittest import mock

import modelica_interface.run_omc as omc_runner
import settings.om_home as om_home

RELEASE = "OPENMODELICAHOME_1_27_0"
MAINTENANCE = "OPENMODELICAHOME_1_27_0_5_g0123456789"
NIGHTLY_OLD = "OPENMODELICAHOME_1_28_0_dev_900_gaaaaaaaaaa"
NIGHTLY = "OPENMODELICAHOME_1_28_0_dev_1962_g6e348e217c"


class TestsOMHome(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self.environ = {name: self.install(name) for name in (NIGHTLY_OLD, RELEASE, NIGHTLY, MAINTENANCE)}

    def tearDown(self):
        shutil.rmtree(self._temp_dir)

    def install(self, name):
        omhome = os.path.join(self._temp_dir, name)
        os.makedirs(os.path.join(omhome, "bin"))
        open(os.path.join(omhome, "bin", "omc.exe"), "w").close()
        return omhome

    def test_versions_newest_first(self):
        self.environ["OPENMODELICAHOME"] = self.environ[RELEASE]
        self.environ["OPENMODELICAHOME_1_30_0"] = os.path.join(self._temp_dir, "uninstalled")
        self.environ["PATH"] = "/usr/bin"
        self.assertEqual(list(om_home.installedVersions(self.environ)), [NIGHTLY, NIGHTLY_OLD, MAINTENANCE, RELEASE])

    def test_versions_number_not_string_order(self):
        names = ["OPENMODELICAHOME_1_9_0", "OPENMODELICAHOME_1_27_1", "OPENMODELICAHOME_1_100_0"]
        environ = {name: self.install(name) for name in names}
        self.assertEqual(list(om_home.installedVersions(environ)), list(reversed(names)))

    def test_openmodelicahome(self):
        self.environ["OPENMODELICAHOME"] = self.environ[RELEASE]
        self.assertEqual(om_home.findOMHome(self.environ), self.environ[RELEASE])

    def test_openmodelicahome_only_is_used_as_it_is(self):
        self.assertEqual(om_home.findOMHome({"OPENMODELICAHOME": "/not/checked"}), "/not/checked")

    def test_openmodelicahome_of_uninstalled_version(self):
        self.environ["OPENMODELICAHOME"] = os.path.join(self._temp_dir, "uninstalled")
        self.assertEqual(om_home.findOMHome(self.environ), self.environ[NIGHTLY])

    def test_newest_version(self):
        self.assertEqual(om_home.findOMHome(self.environ), self.environ[NIGHTLY])

    def test_path(self):
        omhome = self.install("onpath")
        os.chmod(os.path.join(omhome, "bin", "omc.exe"), 0o755)
        os.rename(os.path.join(omhome, "bin", "omc.exe"), os.path.join(omhome, "bin", "omc"))
        if platform.system() != "Windows":
            self.assertEqual(om_home.findOMHome({"PATH": os.path.join(omhome, "bin")}), omhome)

    def test_not_found(self):
        self.assertIsNone(om_home.findOMHome({"PATH": self._temp_dir}))

    def test_names_are_case_insensitive(self):
        self.assertEqual(om_home.findOMHome({"OpenModelicaHome_1_27_0": self.environ[RELEASE]}), self.environ[RELEASE])

    def test_interpreter_windows(self):
        with mock.patch("platform.system", return_value="Windows"):
            with mock.patch.dict(os.environ, {"OPENMODELICAHOME": "C:\\OpenModelica\\"}, clear=True):
                self.assertEqual(omc_runner.interpreterForCurrentPlatform(), '"C:\\OpenModelica\\bin\\omc"')
            with mock.patch.dict(os.environ, {RELEASE: self.environ[RELEASE]}, clear=True):
                self.assertEqual(omc_runner.interpreterForCurrentPlatform(),
                                 '"{0}\\bin\\omc"'.format(self.environ[RELEASE]))
            with mock.patch.dict(os.environ, {"PATH": self._temp_dir}, clear=True):
                self.assertEqual(omc_runner.interpreterForCurrentPlatform(), "omc")

    def test_interpreter_linux(self):
        with mock.patch("platform.system", return_value="Linux"):
            self.assertEqual(omc_runner.interpreterForCurrentPlatform(), "omc")
