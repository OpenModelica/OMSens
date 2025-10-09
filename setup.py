# -*- coding: utf-8 -*-

__license__ = """
This file is part of OpenModelica.
Copyright (c) 1998-CurrentYear, Open Source Modelica Consortium (OSMC),
c/o Linköpings universitet, Department of Computer and Information Science,
SE-58183 Linköping, Sweden.

All rights reserved.

THIS PROGRAM IS PROVIDED UNDER THE TERMS OF GPL VERSION 3 LICENSE OR
THIS OSMC PUBLIC LICENSE (OSMC-PL) VERSION 1.2.
ANY USE, REPRODUCTION OR DISTRIBUTION OF THIS PROGRAM CONSTITUTES
RECIPIENT'S ACCEPTANCE OF THE OSMC PUBLIC LICENSE OR THE GPL VERSION 3,
ACCORDING TO RECIPIENTS CHOICE.

The OpenModelica software and the Open Source Modelica
Consortium (OSMC) Public License (OSMC-PL) are obtained
from OSMC, either from the above address,
from the URLs: http://www.ida.liu.se/projects/OpenModelica or
http://www.openmodelica.org, and in the OpenModelica distribution.
GNU version 3 is obtained from: http://www.gnu.org/copyleft/gpl.html.

This program is distributed WITHOUT ANY WARRANTY; without
even the implied warranty of  MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE, EXCEPT AS EXPRESSLY SET FORTH
IN THE BY RECIPIENT SELECTED SUBSIDIARY LICENSE CONDITIONS OF OSMC-PL.

See the full OSMC Public License conditions for more details.
"""
__author__ = "Adeel Asghar, adeel.asghar@liu.se"

import sys
from pathlib import Path
# Add src folder to sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from OMSens.build_hooks import CustomBuildPy
from setuptools import setup
from wheel.bdist_wheel import bdist_wheel

class wheel(bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False  # mark as platform-specific

setup(
    cmdclass={"build_py": CustomBuildPy, "bdist_wheel": wheel}
)
