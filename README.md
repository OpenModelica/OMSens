# OMSens

OpenModelica sensitivity analysis and optimization module.

## Dependencies

  - [OpenModelica](https://github.com/OpenModelica/OpenModelica)
  - [Python >= 3.6](https://www.python.org/)
  - [Python setuptools](https://pypi.org/project/setuptools/)

## Supported platforms

  - Windows
  - Linux

## Build/Install instructions

Follow the instructions matching your OS:

  - [OMCompiler/README.Linux.md](https://github.com/OpenModelica/OpenModelica/blob/master/OMCompiler/README.Linux.md)
  - [OMCompiler/README.Windows.md](https://github.com/OpenModelica/OpenModelica/blob/master/OMCompiler/README.Windows.md)

### Windows MSYS Makefiles

If you used MSYS Makefiles to compile OpenModelica you need one additional step:

Start a MSYS terminal `$OMDEV\tools\msys\mingw64.exe` (64 bit) or
`$OMDEV\tools\msys\mingw32.exe` (32 bit) and run:

```bash
$ cd /path/to/OpenModelica
make -f Makefile.omdev.mingw omsens -j<Nr. of cores>
```

### Linux

Install the dependencies mentioned above and then run the following commands in the `terminal`.

```bash
$ cd /path/to/OpenModelica/OMSens
$ python setup.py install
```

**Hint**: To find the installation path run `OMEdit` and then go to `Help->About OMEdit`.

## Bug Reports

  - Submit bugs through the [OpenModelica GitHub issues](https://github.com/OpenModelica/OpenModelica/issues/new).
  - [Pull requests](../../pulls) are welcome ❤️
