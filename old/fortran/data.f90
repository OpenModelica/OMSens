module testData
  integer nparams,stopTime,ntarget_vars
  DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE ::  params_values, bl, bu,  wa
  INTEGER, DIMENSION(:), ALLOCATABLE ::  jbound
  CHARACTER(LEN=1000), DIMENSION(:), ALLOCATABLE ::  params_names,target_vars
  DOUBLE PRECISION fopt
  SAVE
  contains
end module testData
