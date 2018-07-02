      subroutine w3Wrapper(stopTime,params_names,params_values,
     *target_vars,nparams,nvars,res_vars_values)
C Inputs:
C        stopTime     = the stopTime of the simulation and also the year from which we will get the variable(s) output
C        params_names  = list of parameters names to perturb to find the maximum (or min) of the function
C        params_values  = list of values of params_names parameters (in the first call to this function, it's likely that these will be the default values of the standard run (scen_1))
C        target_vars = the variables whose output in the simulation we are interested in
C        nparams = length of params_names and params_values

C Wrapper that:
c 1) Sets the .xml with the stoptime and desired parameters values
C 2) Runs W3 binary
C 3) Gets the value of the desired variable for the specified stopTime
C 4) Returns the value of the desired variable for the specified stopTime
      CHARACTER*1000 string_to_write,xml_sys_call,file_path,
     *main_cmd_str, xmlorig_cmd_str, xmlnew_cmd_str, params_list_str,
     *params_values_str, xml_origin_path,xml_new_path,
     *params_names(nparams),
     *w3_sys_call,target_vars(nvars),w3_executable_path,
     *result_file_name,values_str_list(nparams),str_temp,
     *stopTime_cmd_str,stopTime_str, pyScriptInput_file_path,
     *readFromFileflag_str,vars_commas,targ_var,var_from_file,
     *output_flag,parse_output_call
      integer stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER syscall_return_value
      INTEGER result_io_id, pyScriptInput_id
      DOUBLE PRECISION val_target_var,dp_temp,temp_var,
     *params_values(nparams),res_vars_values(nvars)
C Define the inputs to the script. I chose to hardcode them here instead
C of being read from a file or from prompt because I didn't want to deal
C with variable legnth arrays using fortran
      !write(*,*) "-- Inside W3Wrapper --"

      w3_executable_path =
     *"SystemDynamics.WorldDynamics.World3.Scenario_1"
      xml_origin_path = "SystemDynamics.World
     *Dynamics.World3.Scenario_1_init.xml"
      xml_new_path =
     *"tmp/SystemDynamics.WorldDynamics.World3.Scenario_1_init.xml"
C Convert the list of values (DOUBLE PRECISION) to strings for the call to the xml editor
      do i=1,nparams
        write(str_temp,*) params_values(i)
        values_str_list(i) = str_temp
      end do
C Convert stopTime (INTEGER) to string for the call to the xml editor
      write(stopTime_str,*) stopTime

CC Result of the simulation file: always in tmp. (it's implicit in the following 2-3 lines)
      result_io_id = 555
      result_file_name = "w3_res.txt"   ! THE "tmp/" folder is implicit! (it's easier for the execution to simply cd to tmp and refer to result_file_name from the relative path from "tmp")
      open(result_io_id,file="tmp/"//TRIM(result_file_name))
      rewind result_io_id ! I have to rewind the file or I get an EOF

C --- OLD: This works if the parameter and values list are short. I leave it here because it may be useful in the future
C  C Create the system call string for generating a modified .xml
C        main_cmd_str = "python searchAndReplaceXML.py"
C        xmlorig_cmd_str =  TRIM("@@xml_origin_path "//xml_origin_path)
C        xmlnew_cmd_str =   TRIM("@@xml_new_path "//xml_new_path)
C        stopTime_cmd_str = TRIM("@@stopTime "//stopTime_str)
C        params_list_str =       "@@pl"
C        params_values_str =       "@@vl"
C        do i=1,nparams
C         params_list_str = TRIM(TRIM(params_list_str) // " " //
C       *params_names(i)) // " "
C         params_values_str = TRIM(TRIM(params_values_str) // " " //
C       * values_str_list(i)) // " "
C        end do
C  C Call the syscall for generating a modified .xml and check it status return code
C  C (It's really ugly but it works and for now it'll do)
C         xml_sys_call = TRIM(TRIM(TRIM(TRIM(TRIM(main_cmd_str) // " " //
C       * TRIM(xmlorig_cmd_str)) // " " // TRIM(xmlnew_cmd_str)) // " " //
C       * TRIM(stopTime_cmd_str) // " " //
C       * TRIM(params_list_str)) // " " // TRIM(params_values_str))
C          write(*,*) "xml_sys_call"
C          write(*,*) xml_sys_call
C          call system(xml_sys_call)
C        syscall_return_value = system(xml_sys_call)
C --- OLD ^
C We write the inputs in the following order separated by a new line: xml_origin_path, xml_new_path, stopTime, params_names, params_values.
      pyScriptInput_id = 556
      pyScriptInput_file_path = "inputSandR.txt"   ! For now this file name is fixed!
      open(pyScriptInput_id,file=TRIM("inputSandR.txt"))
      write(pyScriptInput_id,*) trim(xml_origin_path)
      write(pyScriptInput_id,*) trim(xml_new_path)
      write(pyScriptInput_id,*) stopTime
C Write the params names in a line (strings)
    2 FORMAT((A)," ")
      do ii=1,nparams
        write(pyScriptInput_id,2,advance="no")
     *    trim(params_names(ii))
      end do
C Add a new line because the last write with advance didn't end with a
C new line
      write(pyScriptInput_id,"(A)") ""
C Write the params values in a line (floats)
    3 FORMAT(' ',E16.8)
      do ii=1,nparams
        write(pyScriptInput_id,3,advance="no")
     *    params_values(ii)
      end do
      write(pyScriptInput_id,"(A)") ""       ! for some reason, this line is necessary or the python script will ignore the last line
C Call the script telling it to read from file instead of from command line args
      main_cmd_str = "python searchAndReplaceXML.py"
      readFromFileflag_str = "@@fromFile"
      xml_sys_call = trim(trim(main_cmd_str)// " " 
     * //trim(readFromFileflag_str))
      call system(xml_sys_call)
      rewind pyScriptInput_id ! I have to rewind the file or I get an EOF

C Now, we have a new .xml created in xml_new_path with the specified
C parameters values. We now have to call the binary executable
C  1) Run simulation and obtain full output
C    a) Put the target_vars in a string with the variables separated by commas
      vars_commas = ""
      do itargetvars=1,nvars
        targ_var = target_vars(itargetvars)                  ! get the next var name
        if(itargetvars .EQ. 1) GO TO 4
        vars_commas = TRIM(vars_commas)//","//TRIM(targ_var) ! append this var to the list of vars separated by commas
        go to 5
  4     vars_commas = TRIM(targ_var)                         ! if the first, don't add a comma before this var
  5     continue
      end do
      output_flag = "-output " // TRIM(vars_commas)
C    b) [cd tmp/] and [simulate with flags -noemit and -output] and [send output to full_output.txt]
       w3_sys_call = TRIM(TRIM(TRIM(TRIM("cd tmp/ && ./"//     ! cd to tmp dir where the W3 binary executable and the newly created .xml are
     *TRIM(w3_executable_path))//" -noemit " //
     *" -lv=-LOG_SUCCESS " //
     *TRIM(output_flag)
     *) //" > full_output.txt"))
       call SYSTEM(w3_sys_call)
C  2) Parse the output using sed and tail and write the values of the variables to a file
C    a) Get the tail of the output (this is to skip the warnings of the simulations, if any, and only get the results) : "tail -n 1"
C    b) Delete the first variable that is always stopTime (stopTime=2100,var_1=100,var_2=22,...): "sed 's/^[^,]*,//'"
C    c) Change from "var_1=100,var_2=22" to "var_1\n100\nvar_2\n22" for
C    easier access in Fortran: "sed 's/,\|=/\n\g'"
       parse_output_call = TRIM("cd tmp/ && tail -n 1 full_output.txt |
     * sed 's/^[^,]*,//'| sed 's/,\|=/\n/g' > " //
     * TRIM(result_file_name))        ! write the full output to full_output.txt and then the tail to tail_output.txt
       call system(parse_output_call)
C  3) Read the varialbles output form result_file_name inside tmp/
      do itargetvars=1,nvars
        targ_var = target_vars(itargetvars)                  ! get the next var name
        read(result_io_id,*) var_from_file                   ! read the next var name from file
        IF(TRIM(targ_var).NE.TRIM(var_from_file)) GO TO 999  ! compare the var name from file and from the array and if different exit with error
        read(result_io_id,*, END=999) res_vars_values(itargetvars) ! write the read file to the array of values to return
        !write(*,*) res_vars_values(itargetvars)
        GO TO 7                                              ! go to the end of the do so it continues with the next var (no error raised)
  999   write(*,*) "  ERROR! Invalid config file. Stopping"
        temp_var = 0
        temp_var = 1/temp_var    ! raises an exception so the iteration from CURVI stops
        STOP
    7 continue
      end do
C The "result" of this subroutine is stored in res_vars_values
      return
      end
