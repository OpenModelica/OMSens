TARGET=curvi
FLAGS= -traceback -gen-interfaces -warn interfaces -save -init=zero -fpe0 -check all -fp-model strict -fp-model except
all:
	ifort $(FLAGS)  data.f90 testReader.f90 zxpowl.for Rut.for  Rutf.for Curvif.for w3WrapperFunc.for main.for -o $(TARGET)

clean:
	rm -f *__genmod*
