subroutine readTest(file_path)
  use testData
  implicit none
  CHARACTER(LEN=500) :: file_path
  integer file_id,stat,i,wa_length

  ! Initialize IO id and file
  file_id=2
  open(file_id,file=file_path)
  ! Read number of params
  call assertNextVarInFileIs(file_id,"nparams")
  read(file_id,*, iostat=stat) nparams
  if (stat /= 0) call exitWithError("Error reading value of nparams into memory")
  ! Allocate all structures that depend on number of params
  allocate(params_names(nparams))
  allocate(params_values(nparams))
  allocate(bl(nparams))
  allocate(bu(nparams))
  allocate(jbound(nparams))
  wa_length = 9*nparams+nparams*(nparams+1)/2+nparams*nparams+max(7*nparams-nparams*(nparams+1)/2,0)
  allocate(wa(wa_length))
  ! Continue reading the file
  call assertNextVarInFileIs(file_id,"params_names")
  read(file_id,*, iostat=stat) (params_names(i), i = 1, nparams)
  if (stat /= 0) call exitWithError("Error reading value of params_names into memory")

  call assertNextVarInFileIs(file_id,"params_values")
  read(file_id,*, iostat=stat) (params_values(i), i = 1, nparams)
  if (stat /= 0) call exitWithError("Error reading value of params_values into memory")

  call assertNextVarInFileIs(file_id,"lower_bounds")
  read(file_id,*, iostat=stat) (bl(i), i = 1, nparams)
  if (stat /= 0) call exitWithError("Error reading value of lower_bounds into memory")

  call assertNextVarInFileIs(file_id,"upper_bounds")
  read(file_id,*, iostat=stat) (bu(i), i = 1, nparams)
  if (stat /= 0) call exitWithError("Error reading value of upper_bounds into memory")

  call assertNextVarInFileIs(file_id,"stopTime")
  read(file_id,*, iostat=stat) stopTime
  if (stat /= 0) call exitWithError("Error reading value of stopTime into memory")

  call assertNextVarInFileIs(file_id,"ntarget_vars")
  read(file_id,*, iostat=stat) ntarget_vars
  if (stat /= 0) call exitWithError("Error reading value of ntarget_vars into memory")

  call assertNextVarInFileIs(file_id,"target_vars")
  ! Allocate target vars array
  allocate(target_vars(ntarget_vars))
  ! Read target_vars into array
  read(file_id,*, iostat=stat) (target_vars(i), i = 1, ntarget_vars)
  ! We finished reading the file, so we expect an end of file. If the file continues, exit with error
  if (stat /= 0) call exitWithError("Error reading value of target_vars into memory")

end subroutine readTest

subroutine exitWithError(error_str)
  implicit none
  CHARACTER(LEN=*) :: error_str
    write(*,*) "  ERROR! Invalid config file. Stopping. ", error_str
    STOP
end subroutine exitWithError

subroutine assertNextVarInFileIs(file_id,expected_var)
  implicit none
  CHARACTER(LEN=*) :: expected_var
  CHARACTER(LEN=30) :: VAR_NAME
  integer file_id,stat
  read(file_id,"(A)", iostat=stat) VAR_NAME
  write(*,*) "Reading ", VAR_NAME
  if (stat /= 0) call exitWithError("Error trying to read the name of expected var " // expected_var // " into memory")
  IF(VAR_NAME.NE.expected_var) call exitWithError("Tried to read variable " // expected_var // " bot got var " // VAR_NAME // " instead.")
end subroutine assertNextVarInFileIs
