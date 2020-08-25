#!/usr/bin/env python
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
__maintainer__ = "https://openmodelica.org"
__status__ = "Production"

from setuptools import setup
import os
import sys
import platform
from shutil import which
from subprocess import call
from shutil import copy2

setup(name='OMSens',
      python_requires='>=3.6',
      version='1.0.0',
      description='OpenModelica sensitivity analysis and optimization module',
      author='Rodrigo Castro',
      author_email='rcastro@dc.uba.ar',
      maintainer='Adeel Asghar',
      maintainer_email='adeel.asghar@liu.se',
      license="BSD, OSMC-PL 1.2, GPL (user's choice)",
      url='http://openmodelica.org/',
      install_requires=[
          'six',
          'pytest',
          'matplotlib',
          'numpy',
          'pandas'
      ]
      )

platform_architecture = platform.architecture()[0]

try:
    omhome = os.path.split(os.path.split(os.path.realpath(which("omc")))[0])[0]
except BaseException:
    omhome = None
    omhome = omhome or os.environ.get('OPENMODELICAHOME')

    if sys.platform=="win32":
        omdev = os.environ.get('OMDEV')
        if omdev:
            omhome = omdev

    if omhome is None:
        raise Exception("Failed to find OPENMODELICAHOME (searched for environment variable as well as the omc executable)")

try:
    # Compile CURVI files
    env = os.environ
    if sys.platform=="win32":
        if platform_architecture=="64bit":
            gfortran_env = os.path.join(omhome, "tools", "msys", "mingw64", "bin")
            gfortran_path = os.path.join(gfortran_env, "gfortran.exe")
            env["PATH"] = gfortran_env + ";" + env["PATH"]
        else:
            gfortran_env = os.path.join(omhome, "tools", "msys", "mingw32", "bin")
            gfortran_path = os.path.join(gfortran_env, "gfortran.exe")
            env["PATH"] = gfortran_env + ";" + env["PATH"]
    else:
        gfortran_path = "gfortran"
    if 0 != call([gfortran_path, "-fPIC", "-c", "Rutf.for", "Rut.for", "Curvif.for"], cwd="fortran_interface", env=env):
        raise Exception("Failed to compile CURVI files.")
    print("CURVI files compiled.")

    # Generate CURVIF python binary
    if sys.platform=="win32":
        f2py_path = os.path.join(os.path.dirname(sys.executable), "Scripts", "f2py.exe")
        f2py_call = call([f2py_path, "-c", "-I.", "Curvif.o", "Rutf.o", "Rut.o", "-m", "curvif_simplified", "curvif_simplified.pyf", "Curvif_simplified.f90", "--compiler=mingw32"], cwd="fortran_interface")
    else:
        f2py_path = "f2py"
        f2py_call = call([f2py_path, "-c", "-I.", "Curvif.o", "Rutf.o", "Rut.o", "-m", "curvif_simplified", "curvif_simplified.pyf", "Curvif_simplified.f90"], cwd="fortran_interface")
    if 0 != f2py_call:
        raise Exception("Failed to generate CURVIF python binary.")
    # Following dlls are needed to run curvif_simplified.xxxx-xxxxx.pyd
    if sys.platform=="win32":
        copy2(gfortran_env + "/libgcc_s_seh-1.dll", "./fortran_interface")
        copy2(gfortran_env + "/libgfortran-3.dll", "./fortran_interface")
        copy2(gfortran_env + "/libquadmath-0.dll", "./fortran_interface")
        copy2(gfortran_env + "/libwinpthread-1.dll", "./fortran_interface")
    print("Generated CURVIF python binary.")
except ImportError:
    print("Error installing OMSens.")
