Steps for now:
1) Compile CURVI files:
    gfortran -fPIC -c Rutf.for Rut.for Curvif.for
2) Using:
   a) Curvi compiled files from prev point(s)
   b) Curvi wrapper f90 file
   c) Curvi wrapper pyf modified by Ale
   Run:
    f2py -c -I. Curvif.o Rutf.o Rut.o -m curvif_simplified curvif_simplified.pyf Curvif_simplified.f90
