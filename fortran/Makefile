TARGET=curvi
FLAGS= -traceback -gen-interfaces -warn interfaces -save -init=zero -fpe0 -check all -fp-model strict -fp-model except
# Flags 64 bits: DA MUY DISTINTO!!!
# FLAGS= -gen-interfaces -warn uncalled -warn interfaces -save -init=zero -fpe0 -traceback -check all -integer_size 64 -real_size 64
# EXTRA_FILES =  $(wildcard extras/*)
# FUNCS_FILES= $(wildcard primary/*)
# DATA_SHARED_FILES = $(wildcard DATA/shared_vars/*)
# DATA_LOCAL_FILES = $(wildcard DATA/local_vars/*)
# MONITORS_FILES = $(wildcard monitors/*)
# MODEL_FILE = model.for
# MAIN_FILE = main.for
# all: csv_file.o
all:
	ifort $(FLAGS)  data.f90 test_template.f90  zxpowl.for Rut.for  Rutf.for Curvif.for w3WrapperFunc.for main.for -o $(TARGET)

clean:
	rm -f *.mod
	rm -f *.o
