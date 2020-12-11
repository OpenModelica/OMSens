# OMSens

OpenModelica sensitivity analysis and optimization module.

## Dependencies

- [OpenModelica](https://openmodelica.org)
- [Python >= 3.6](https://www.python.org/)
- [Python setuptools](https://pypi.org/project/setuptools/)

## Supported platforms

- Windows
- Linux

## Build/Install instructions

### Windows

OMSens is installed automatically with OpenModelica on Windows.
If you still want to build it then setup the [Windows environment](https://github.com/OpenModelica/OpenModelica/blob/master/OMCompiler/README-OMDev-MINGW.md).
Once the environment is ready then run the makefile.

```bash
cd /path/to/OpenModelica
make -f Makefile.omdev.mingw omsens
```

OR

```bash
cd /path/to/OpenModelica/OMSens
make -f Makefile.omdev.mingw OMBUILDDIR=/path/to/OpenModelica/builddirectory
```

### Linux

Install the dependencies mentioned above and then run the following commands in the `terminal`.

```bash
$ cd /path/to/OpenModelica/OMSens
$ python setup.py install
```

**Hint**: To find the installation path run `OMEdit` and then go to `Help->About OMEdit`.

## Bug Reports

- Submit bugs through the [issues](issues).
- [Pull requests](pulls) are welcome.
