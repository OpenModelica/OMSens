# Where to find OpenModelica if several versions are installed.
#
# The Windows installer keeps OPENMODELICAHOME for the version selected as the default one and sets
# OPENMODELICAHOME_<version> for each installed version, with every character of the version that is not a
# letter or a digit replaced by an underscore: version 1.27.0 is found via OPENMODELICAHOME_1_27_0.
#
# Only the standard library is used, build_hooks.py loads this file while the package is built.
import os
import shutil
from pathlib import Path

OMHOME_ENV = "OPENMODELICAHOME"
OMHOME_ENV_VERSION_PREFIX = OMHOME_ENV + "_"


def hasOMC(omhome):
    omhome = Path(omhome)
    return (omhome / "bin" / "omc").is_file() or (omhome / "bin" / "omc.exe").is_file()


def versionSortKey(name):
    # Sort key for the names OPENMODELICAHOME_<version>; the newest version has the highest key.
    # The version is <major>_<minor>_<patch> followed by nothing for a release (1_27_0), by a pre-release part
    # for a build before that release (1_28_0_dev_1962_g6e348e217c) or by the number of commits for a build
    # after that release (1_27_0_5_g0123456789). For the same <major>_<minor>_<patch> a pre-release is older
    # than the release, which is older than a build after it; the numbers that follow decide between two
    # builds of the same kind.
    parts = name[len(OMHOME_ENV_VERSION_PREFIX):].split("_")
    numbers = []
    while parts and parts[0].isdigit() and len(numbers) < 3:
        numbers.append(int(parts.pop(0)))
    numbers += [0] * (3 - len(numbers))
    if not parts:
        kind = 1  # release
    elif parts[0].isdigit():
        kind = 2  # commits after the release
    else:
        kind = 0  # dev, alpha, beta, rc, ...
    return tuple(numbers), kind, tuple(int(part) for part in parts if part.isdigit())


def installedVersions(environ=None):
    # The installations registered as OPENMODELICAHOME_<version>, newest version first, as a dict from the name
    # of the environment variable to the installation directory. Variables which point to a directory without
    # an omc executable are left out.
    if environ is None:
        environ = os.environ
    homes = {}
    for name, value in environ.items():
        # the names of environment variables are case-insensitive on Windows
        if name.upper().startswith(OMHOME_ENV_VERSION_PREFIX) and value and hasOMC(value):
            homes[name] = value
    return dict(sorted(homes.items(), key=lambda item: versionSortKey(item[0]), reverse=True))


def findOMHome(environ=None):
    # The installation directory of the OpenModelica to use, None if there is none. The first one that applies:
    #  1. OPENMODELICAHOME, if there is an omc executable in it
    #  2. the newest OPENMODELICAHOME_<version>
    #  3. the installation of the omc on the PATH
    if environ is None:
        environ = os.environ
    versions = installedVersions(environ)
    omhome = environ.get(OMHOME_ENV)
    # Without versioned installations the path is used as it is, as it always was. With them, a path left
    # behind by an uninstalled version is skipped.
    if omhome and (not versions or hasOMC(omhome)):
        return omhome
    if versions:
        return next(iter(versions.values()))
    omc_executable = shutil.which("omc", path=environ.get("PATH"))
    if omc_executable:
        return str(Path(omc_executable).parent.parent)
    return None
