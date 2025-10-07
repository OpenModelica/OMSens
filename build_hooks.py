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

import shutil
import subprocess
import sys
from pathlib import Path
from setuptools.command.build_py import build_py as _build_py

# Fortran sources and f2py files
FORTRAN_FILES = ["Rutf.for", "Rut.for", "Curvif.for"]
FPY_FILES = ["curvif_simplified.pyf", "Curvif_simplified.f90"]

# Directory where Fortran sources live
FORTRAN_DIR = Path(__file__).parent / "src" / "OMSens" / "fortran_interface"

class CustomBuildPy(_build_py):
    """Custom build_py to compile Fortran and f2py into the source package folder."""

    def run(self):
        # locate OpenModelica installation
        omhome = None
        omc_executable = shutil.which("omc")
        if omc_executable:
            # Get the directory two levels up from omc executable
            omc_dir = Path(omc_executable).parent
            omhome = omc_dir.parent
        else:
            # Fallback to environment variable
            omhome = subprocess.os.environ.get("OPENMODELICAHOME")
            if not omhome:
                raise RuntimeError("Failed to find OPENMODELICAHOME (searched for environment variable as well as the omc executable).")

        omdev = None
        # locate gfortran
        if subprocess.os.name == "nt":
            # Try to get gfortran from OMDEV environment variable
            omdev = subprocess.os.environ.get("OMDEV")
            if omdev:
                gfortran_executable = Path(omdev) / "tools" / "msys" / "ucrt64" / "bin" / "gfortran.exe"
            else:
                # Set the gfortran path based on OPENMODELICAHOME for Windows
                gfortran_executable = Path(omhome) / "tools" / "msys" / "ucrt64" / "bin" / "gfortran.exe"
            gfortran_executable = str(gfortran_executable) if Path(gfortran_executable).exists() else None
        else:
            gfortran_executable = shutil.which("gfortran")
        if not gfortran_executable:
            raise RuntimeError("Failed to find gfortran executable in PATH.")

        # Prepare f2py command
        f2py_cmd = [
            sys.executable, "-m", "numpy.f2py",
            "-c",
            "-I.",
            *FORTRAN_FILES,
            *FPY_FILES,
            "-m", "curvif_simplified"
        ]

        # Remove empty strings (in case any are present)
        f2py_cmd = [arg for arg in f2py_cmd if arg]

        # Set environment for f2py
        env = subprocess.os.environ.copy()
        if subprocess.os.name == "nt":
            gfortran_dir = str(Path(gfortran_executable).parent)
            env["PATH"] = gfortran_dir + subprocess.os.pathsep + env.get("PATH", "")

        subprocess.check_call(f2py_cmd, cwd=FORTRAN_DIR, env=env)

        # Copy required DLLs on Windows
        if subprocess.os.name == "nt":
            binaries_path = None
            if omdev:
                binaries_path = Path(omdev) / "tools" / "msys" / "ucrt64" / "bin"
            else:
                binaries_path = Path(omhome) / "tools" / "msys" / "ucrt64" / "bin"
            if not binaries_path.exists():
                raise RuntimeError("OM_MSYS_ENV_DIR environment variable not set or directory does not exist.")
            dll_patterns = [
                "libgcc_s_*.dll",
                "libgfortran*.dll",
                "libquadmath*.dll",
                "libwinpthread*.dll"
            ]

            for pattern in dll_patterns:
                for dll_path in binaries_path.glob(f"{pattern}"):
                    shutil.copy2(dll_path, FORTRAN_DIR)

        super().run()
