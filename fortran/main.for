c     Usage:  call fu(n,x,f)
c         n:  dimension of x.
c         x:  n-dimensional vector.
c         f:  value of the function at the point x.    ! Ale: fx en nugrad
c
c         n:  dimension of the problem.
c
c        x0:  initial guess point.
c
c       eps:  tolerance for the stopping criterion.
c
c    ibound:  parameter such that if equal to
c             0 is an unconstrained problem
c             1 is a constrained problem.
c
c    jbound:  working vector of dimension n defining the sort of
c             constraint for each variable (only used when ibound.ne.0).
c             jbound(i) = 0 if the ith variable has no constraints.
c                         1 if the ith variable has only upper bounds.
c                         2 if the ith variable has only lower bounds.
c                         3 if the ith variable has both upper and
c                           lower bounds.
c
c        bl:  vector of lower bounds (not used if ibound=0).
c
c        bu:  vector of upper bounds (not used if ibound=0).
c
c        wa:  working vector of dimension (see output)
c             9*n+n*(n+1)/2+n*n+max(7*n-n*(n+1)/2,0)
c
c       nfu:  maximum number of function evaluations. If equal to
c             zero, the default value of 5000*n is used.
c
c     idiff:  Choose forward or central differences.  Forward
c            differences require fewer function evaluations and
c             should be favored unless the problem is exceedingly
c             difficult.
c             idiff = 1  forward differences
c             idiff = 2  central differences
c
c     kmax:   The parameter kmax is such that the hessian is
c             recomputed every kmax iterations.
c             We recommend kmax = 3 unless the problem is
c             very difficult.  In this case choose kmax = 1 or 2.
      program main
        use testData
        implicit none
      CHARACTER(LEN=500) :: infile_path,tests_path,file_name,
     * raw_infile_path, raw_outfile_path, outfile_path
      integer i, ibound, nfu, idiff, kmax, nit, ier,argsize
      integer output_id
      double precision eps
      external objectiveFunction

      ! Define which test to run

      ! Read test to run from command line
      CALL getarg(1, raw_infile_path)
      argsize = LEN_TRIM(raw_infile_path)
      IF(argsize .EQ. 0) call exitWithError("Invalid input command line
     * arguments. Should be two: input file and output file
     *Example: tests/test_01.txt tmp/output.csv")
      infile_path = TRIM(raw_infile_path)
      ! Read output file path from command line
      CALL getarg(2, raw_outfile_path)
      argsize = LEN_TRIM(raw_outfile_path)
      IF(argsize .EQ. 0) call exitWithError("Invalid input command line
     * arguments. Should be two: input file and output file
     *Example: tests/test_01.txt tmp/output.csv")
      outfile_path = TRIM(raw_outfile_path)

      ! Hardcode the test to run
!      tests_path = "tests/"
!      file_name = "test_01.txt"
!      !file_name = "test_10.txt"
!      infile_path = trim(tests_path) // trim(file_name)

      ! Read test file
      call readTest(infile_path)

      ! Initialize CURVI inputs that are used with the same value for every test
      eps=1.d-10    ! tolerance for the stopping criterion.
      ibound=1      ! 1 if constrained problem
      nfu=0         ! max number of calls to fu
      idiff=2       ! idiff = 2  central differences
      kmax=3        ! hessian is recomputed after kmax iterations
      DO i=1,nparams
        jbound(i)=3      ! 3 if the ith variable has both upper and lower bounds
      end do

      ! Call curvi:
      call curvif(objectiveFunction, ! fu
     * nparams,                      ! n
     * params_values,                ! x0
     * fopt,                         ! fopt
     * eps,
     * ibound,
     * jbound,
     * bl,
     * bu,
     * wa,
     * nfu,
     * nit,
     * idiff,
     * kmax,
     * ier)

      ! Open output file to output_id
      output_id = 555
      open(output_id,file=outfile_path)
      ! Write header
      write(output_id,"(A)")'"Parameter_name", "Parameter_value"'
      ! Write values for each parameter
      do i=1,nparams
        write(output_id,"(9999(A,',',G12.5))")trim(params_names(i)),
     * params_values(i)
      end do
      ! Log to stdout that we wrote the result
      write(*,*)" Wrote optimal parameter values to ",trim(outfile_path)

      ! Deallocate everything and exit
      deallocate(params_names)
      deallocate(params_values)
      deallocate(bl)
      deallocate(bu)
      deallocate(jbound)
      deallocate(wa)
      deallocate(target_vars)

C  Curvi single variable cost function using only population:
!      call test01()  ! only nr_resources_init
C      call test02()
C      call test03()  !relative top12 for 5% and modifying here 5%
C      call test04()  !relative top12 for 5% and modifying here 1%
C      call test05()  !perturb all of the params by max of +-1%   (ran for a day and didn't finish)
C      call test06()     !relative top18 (>1% effect) for 5% and modifying here 3%
C      call test07()     !relative no influencers curvi 5%
C      call test08()     !relative top36 (>0.1% effect) for 5% and modifying here 3%
C      call test09()     ! only measurable initial values (initial values of variables that model the real life) curvi 3%
C      call test10()     ! only measurable initial values (initial values of variables that model the real life) curvi 5%
C  Curvi multi variable cost function:
C      call test23()     ! equivalent to test 03 but also taking into account hwi alongside pop
C      call test24()     ! SIMILAR to test 04 but 3% INSTEAD OF 1% also taking into account hwi alongside pop
C      call test26()     ! equivalent to test 06 but also taking into account hwi alongside pop
C Using ZXPOWL:
C      call test11()   ! equivalent to test01 but zxpowl instead of curvi
C      call test16()   ! equivalent to test06 but zxpowl instead of curvi
C Trying to maximize only hdi:
C      call test31()   ! the parameters are the policy triggers for scenarios 2 to 9. Initial: 2050
C      call test32()   ! the parameters are the policy triggers for scenarios 2 to 9. Initial: 2018
C      call test33()   ! the parameters are the policy triggers for scenarios 2 to 9. Initial: 2034

C BORRAR :
C      DOUBLE PRECISION params_values(1),x(1)
C      DOUBLE PRECISION f
C      params_values = (/1000000000000.0D0/)      !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
C      x = params_values
C      n = 1
C       call fu_test10(n,x,f)
C BORRAR ^
      end program

      subroutine objectiveFunction(n,x,f)
        use testData ! where we get the common vars
        implicit none
      DOUBLE PRECISION x(n), res_vars_values(1), f
      integer n

      call w3Wrapper(stopTime,
     * params_names,x,target_vars,nparams,
     * ntarget_vars,res_vars_values)
      !  For now the objective function allows only one output variable
      !  and it tries to maximize it (by negating it as CURVI is a
      !  minimizer). An example of a more complex objective function
      !  could be: "f = -(res_vars_values(1)/1D10 + res_vars_values(2))",
      !  that uses 2 variables instead of one.
      f = -res_vars_values(1)
      write(*,*) "Objective function value:"
      write(*,*) f
      return
      end subroutine objectiveFunction



C .--------------------------------------------------------------------------------- DESCOMENTAR:

C--------------- Test01 -----------------
      subroutine test01()
      DOUBLE PRECISION params_values(1)
      dimension jbound(1)
      DOUBLE PRECISION bl(1),bu(1),x0(1),wa(17),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test01

        write(*,*) "Inside test01 at date:"
        call system("date")
      params_values = (/1000000000000.0D0/)      !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 1
      eps=1.d-10
      ibound=1
      jbound(1)=3      ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
C      jbound(2)=3
      bl(1)=1000D0     ! lower bound of x0(1) (depends on ibound and jbound)
C      bl(2)=-3.d0
      bu(1)=2000000000000.0D0    ! upper bound of x0(1)  (depends on ibound and jbound)
C      bu(2)=3.d0
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test01, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)x0(1)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test01 at date:"
        call system("date")
      end subroutine test01
C Test01: fu
      subroutine fu_test01(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      integer nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f

      nvars = 1
      stopTime = 2100
      params_names = (/"nr_resources_init"/)    !careful! you have to change the list length on top if you add or remove a parameter
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine
C--------------- Test02 -----------------
C# Hugo Scolnik article: "Crítica metodológica al modelo WORLD 3" (Methodological criticisim to the World3 model)
C#   Perturbed 5 params by 5%
C      # ICOR= 3.15, Default: ICOR=3
C      # ALIC= 13.3, Default: ALIC=14
C      # ALSC= 17.1, Default: ALSC=20
C      # SCOR= 1.05, Default: SCOR=1
C      # Run "Perturbed": FFW= 0.231, Default: FFW=0.22
C      # Run "Perturbed Increasing FFW": FFW= 0.242, Default: FFW=0.22
C#   Perturbed rest of the params by a scalar of 0.24172080E-12
C In this test:
C    We run the function trying to maximize the population by perturbing ICOR(p_ind_cap_out_ratio_1), ALIC(p_avg_life_ind_cap_1), ALSC(p_avg_life_serv_cap_1) and SCOR(p_serv_cap_out_ratio_1).

      subroutine test02()
      DOUBLE PRECISION params_values(4)
      dimension jbound(4)
      DOUBLE PRECISION bl(4),bu(4),x0(4),wa(80),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test02
C p_ind_cap_out_ratio_1,3
        write(*,*) "Inside test02 at date:"
        call system("date")
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1
      params_values = (/3D0,14D0,20D0,1D0/)      !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 4
      eps=1.d-10
      ibound=1
      jbound(1)=3      ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      jbound(2)=3
      jbound(3)=3
      jbound(4)=3
C Lower bounds: -5% than default
      bl(1)= 2.85        ! lower bound of x0(1) (depends on ibound and jbound)
      bl(2)= 13.3
      bl(3)= 19.0
      bl(4)= 0.95
C Upper bounds: +5% than default
      bu(1)= 3.15        ! upper bound of x0(1) (depends on ibound and jbound)
      bu(2)= 14.7
      bu(3)= 21
      bu(4)= 1.05

      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test02, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)x0(1),x0(2),x0(3),x0(4)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test02 at date:"
        call system("date")
      end subroutine test02
C Test02: fu
      subroutine fu_test02(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(4), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      integer nvars
      DOUBLE PRECISION x(4)
      DOUBLE PRECISION res_vars_values(1), params_values(4),f
      write(*,*) "*** Inside fu_test02!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      nvars = 1
      stopTime = 2100
      params_names(1)  = "p_ind_cap_out_ratio_1"
      params_names(2)  = "p_avg_life_ind_cap_1"
      params_names(3)  = "p_avg_life_serv_cap_1"
      params_names(4)  = "p_serv_cap_out_ratio_1"
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine


C--------------- Test03 -----------------
C This test optimizes population by perturbing the "top 12 parameters" by 5%
C from the relative index. "Top" in the sense of the most influencers of
C the variable population.
C                               DEFAULT            Value WP2         Description
C        max_tot_fert_norm       & 12.0           & 12.60          & "Normal maximal total fertility"                                 \\
C        p_fioa_cons_const_1     & 0.43           & 0.45           & "Default frac of industrial output allocated to consumption" \\
C        p_ind_cap_out_ratio_1   & 3.0            & 3.15           & "Default industrial capital output ratio"                        \\
C        p_serv_cap_out_ratio_1  & 1.0            & 1.05           & "Default fraction of service sector output ratio"                \\
C        life_expect_norm        & 28.0           & 29.40          & "Normal life expectancy"                                         \\
C        des_compl_fam_size_norm & 3.8            & 4.00           & "Desired normal complete family size"                            \\
C        industrial_capital_init & 210000000000.0 & 199500000000.0 & "Initial industrial investment"                       \\
C        p_land_yield_fact_1     & 1.0            & 0.95           & "Default land yield factor"                           \\
C        p_nr_res_use_fact_1     & 1.0            & 0.95           & "Default non-recoverable resource utilization factor" \\
C        reproductive_lifetime   & 30.0           & 28.5           & "Reproductive life time"                              \\
C        subsist_food_pc         & 230.0          & 218.5          & "Available per capita food"                           \\
C        p_avg_life_ind_cap_1    & 14.0           & 13.29          & "Default average life of industrial capital";         \\
      subroutine test03()
      DOUBLE PRECISION params_values(12)
      dimension jbound(12)
      DOUBLE PRECISION bl(12),bu(12),x0(12),wa(336),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test03
        write(*,*) "Inside test03 at date:"
        call system("date")
      params_values = (/12.0D0, 0.43D0, 3.0D0, 1.0D0, 28.0D0,
     *3.8D0, 210000000000.0D0, 1.0D0, 1.0D0, 30.0D0, 230.0D0,
     *14.0D0/) !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 12
      eps=1.d-10
      ibound=1
      do ijbound=1,12
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,12
C Lower bounds: -5% than default
        bl(iparams) = params_values(iparams)*0.95
C Upper bounds: +5% than default
        bu(iparams) = params_values(iparams)*1.05
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test03, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 12)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test03 at date:"
        call system("date")
      end subroutine test03
C Test03: fu
      subroutine fu_test03(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(12), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test03!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i":
      params_names(1) = "max_tot_fert_norm"
      params_names(2) = "p_fioa_cons_const_1"
      params_names(3) = "p_ind_cap_out_ratio_1"
      params_names(4) = "p_serv_cap_out_ratio_1"
      params_names(5) = "life_expect_norm"
      params_names(6) = "des_compl_fam_size_norm"
      params_names(7) = "industrial_capital_init"
      params_names(8) = "p_land_yield_fact_1"
      params_names(9) = "p_nr_res_use_fact_1"
      params_names(10) = "reproductive_lifetime"
      params_names(11) = "subsist_food_pc"
      params_names(12) = "p_avg_life_ind_cap_1"
C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine


C--------------- Test04 -----------------
C SIMILAR TO TEST03 BUT 1% INSTEAD OF 5%
C This test optimizes population by perturbing the "top 12 parameters" by 5%
C from the relative index. "Top" in the sense of the most influencers of
C the variable population.
C                               DEFAULT            Value WP2         Description
C        max_tot_fert_norm       & 12.0           & 12.60          & "Normal maximal total fertility"                                 \\
C        p_fioa_cons_const_1     & 0.43           & 0.45           & "Default frac of industrial output allocated to consumption" \\
C        p_ind_cap_out_ratio_1   & 3.0            & 3.15           & "Default industrial capital output ratio"                        \\
C        p_serv_cap_out_ratio_1  & 1.0            & 1.05           & "Default fraction of service sector output ratio"                \\
C        life_expect_norm        & 28.0           & 29.40          & "Normal life expectancy"                                         \\
C        des_compl_fam_size_norm & 3.8            & 4.00           & "Desired normal complete family size"                            \\
C        industrial_capital_init & 210000000000.0 & 199500000000.0 & "Initial industrial investment"                       \\
C        p_land_yield_fact_1     & 1.0            & 0.95           & "Default land yield factor"                           \\
C        p_nr_res_use_fact_1     & 1.0            & 0.95           & "Default non-recoverable resource utilization factor" \\
C        reproductive_lifetime   & 30.0           & 28.5           & "Reproductive life time"                              \\
C        subsist_food_pc         & 230.0          & 218.5          & "Available per capita food"                           \\
C        p_avg_life_ind_cap_1    & 14.0           & 13.29          & "Default average life of industrial capital";         \\
      subroutine test04()
      DOUBLE PRECISION params_values(12)
      dimension jbound(12)
      DOUBLE PRECISION bl(12),bu(12),x0(12),wa(336),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test04
C p_ind_cap_out_ratio_1,3
        write(*,*) "Inside test04 at date:"
        call system("date")
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1
      params_values = (/12.0D0, 0.43D0, 3.0D0, 1.0D0, 28.0D0,
     *3.8D0, 210000000000.0D0, 1.0D0, 1.0D0, 30.0D0, 230.0D0,
     *14.0D0/) !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 12
      eps=1.d-10
      ibound=1
      do ijbound=1,12
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,12
C Lower bounds: -1% than default
        bl(iparams) = params_values(iparams)*0.99
C Upper bounds: +1% than default
        bu(iparams) = params_values(iparams)*1.01
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test04, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 12)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test04 at date:"
        call system("date")
      end subroutine test04
C Test04: fu
      subroutine fu_test04(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(12), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test04!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i":
      params_names(1) = "max_tot_fert_norm"
      params_names(2) = "p_fioa_cons_const_1"
      params_names(3) = "p_ind_cap_out_ratio_1"
      params_names(4) = "p_serv_cap_out_ratio_1"
      params_names(5) = "life_expect_norm"
      params_names(6) = "des_compl_fam_size_norm"
      params_names(7) = "industrial_capital_init"
      params_names(8) = "p_land_yield_fact_1"
      params_names(9) = "p_nr_res_use_fact_1"
      params_names(10) = "reproductive_lifetime"
      params_names(11) = "subsist_food_pc"
      params_names(12) = "p_avg_life_ind_cap_1"
C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine
C--------------- Test05 -----------------
C Optimize ALL the params by 1%
      subroutine test05()
      DOUBLE PRECISION params_values(96)
      dimension jbound(96)
      DOUBLE PRECISION bl(96),bu(96),x0(96),wa(14736),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test05
        write(*,*) "Inside test05 at date:"
        call system("date")
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1
      params_values = (/ 5000000000.0D0, 1.0D0, 900000000.0D0, 1.5D0,
     * 1000.0D0, 3.8D0, 2.0D0, 1.2D0, 4800000000.0D0, 2.0D0, 0.001D0,
     * 0.02D0, 20.0D0, 3.0D0, 0.1D0, 10.0D0, 790000000000.0D0, 400.0D0,
     * 210000000000.0D0, 600.0D0, 0.75D0, 1.0D0, 2.0D0, 600.0D0, 0.7D0,
     * 28.0D0, 20.0D0, 12.0D0, 1000000000000.0D0, 2.0D0, 2.0D0, 14.0D0,
     * 14.0D0, 20.0D0, 20.0D0, 0.43D0, 0.43D0, 1.0D0, 0.2D0, 0.1D0,
     * 0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0,
     * 3.0D0, 1.0D0, 1.0D0, 1.0D0, 0.0D0, 0.0D0, 0.0D0, 0.0D0, 0.0D0,
     * 0.0D0, 0.0D0, 0.0D0, 1.0D0, 1.0D0, 0.0D0, 0.0D0, 0.0D0, 0.0D0,
     * 1.0D0, 25000000.0D0, 650000000.0D0, 700000000.0D0, 190000000.0D0,
     * 60000000.0D0, 2300000000.0D0, 3200000000.0D0, 136000000.0D0,
     * 1.0D0, 20.0D0, 0.1D0, 30.0D0, 1.0D0, 144000000000.0D0, 20.0D0,
     * 0.07D0, 230.0D0, 4000.0D0, 4000.0D0, 4000.0D0, 4000.0D0,
     * 4000.0D0, 4000.0D0, 4000.0D0, 4000.0D0, 20.0D0, 10.0D0,
     * 8200000.0D0, 1.0D0 /) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 96
      eps=1.d-10
      ibound=1
      do ijbound=1,96
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,96
C Lower bounds: -1% than default
        bl(iparams) = params_values(iparams)*0.99
C Upper bounds: +1% than default
        bu(iparams) = params_values(iparams)*1.01
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test05, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 96)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test05 at date:"
        call system("date")
      end subroutine test05
C Test05: fu
      subroutine fu_test05(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test05!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i":
      params_names(1)  = "agr_inp_init"
      params_names(2)  = "agr_mtl_toxic_index"
      params_names(3)  = "arable_land_init"
      params_names(4)  = "assim_half_life_1970"
      params_names(5)  = "avg_life_land_norm"
      params_names(6)  = "des_compl_fam_size_norm"
      params_names(7)  = "des_food_ratio_dfr"
      params_names(8)  = "des_ppoll_index_DPOLX"
      params_names(9)  = "des_res_use_rt_DNRUR"
      params_names(10) = "food_short_perc_del"
      params_names(11) = "fr_agr_inp_pers_mtl"
      params_names(12) = "frac_res_pers_mtl"
      params_names(13) = "hlth_serv_impact_del"
      params_names(14) = "income_expect_avg_time"
      params_names(15) = "ind_mtl_emiss_fact"
      params_names(16) = "ind_mtl_toxic_index"
      params_names(17) = "ind_out_in_1970"
      params_names(18) = "ind_out_pc_des"
      params_names(19) = "industrial_capital_init"
      params_names(20) = "inherent_land_fert"
      params_names(21) = "labor_force_partic"
      params_names(22) = "labor_util_fr_del_init"
      params_names(23) = "labor_util_fr_del_time"
      params_names(24) = "land_fertility_init"
      params_names(25) = "land_fr_harvested"
      params_names(26) = "life_expect_norm"
      params_names(27) = "lifet_perc_del"
      params_names(28) = "max_tot_fert_norm"
      params_names(29) = "nr_resources_init"
      params_names(30) = "p_avg_life_agr_inp_1"
      params_names(31) = "p_avg_life_agr_inp_2"
      params_names(32) = "p_avg_life_ind_cap_1"
      params_names(33) = "p_avg_life_ind_cap_2"
      params_names(34) = "p_avg_life_serv_cap_1"
      params_names(35) = "p_avg_life_serv_cap_2"
      params_names(36) = "p_fioa_cons_const_1"
      params_names(37) = "p_fioa_cons_const_2"
      params_names(38) = "p_fr_cap_al_obt_res_2[1]"
      params_names(39) = "p_fr_cap_al_obt_res_2[2]"
      params_names(40) = "p_fr_cap_al_obt_res_2[3]"
      params_names(41) = "p_fr_cap_al_obt_res_2[4]"
      params_names(42) = "p_fr_cap_al_obt_res_2[5]"
      params_names(43) = "p_fr_cap_al_obt_res_2[6]"
      params_names(44) = "p_fr_cap_al_obt_res_2[7]"
      params_names(45) = "p_fr_cap_al_obt_res_2[8]"
      params_names(46) = "p_fr_cap_al_obt_res_2[9]"
      params_names(47) = "p_fr_cap_al_obt_res_2[10]"
      params_names(48) = "p_fr_cap_al_obt_res_2[11]"
      params_names(49) = "p_ind_cap_out_ratio_1"
      params_names(50) = "p_land_yield_fact_1"
      params_names(51) = "p_nr_res_use_fact_1"
      params_names(52) = "p_ppoll_gen_fact_1"
      params_names(53) = "p_ppoll_tech_chg_mlt[1]"
      params_names(54) = "p_ppoll_tech_chg_mlt[2]"
      params_names(55) = "p_ppoll_tech_chg_mlt[3]"
      params_names(56) = "p_ppoll_tech_chg_mlt[4]"
      params_names(57) = "p_res_tech_chg_mlt[1]"
      params_names(58) = "p_res_tech_chg_mlt[2]"
      params_names(59) = "p_res_tech_chg_mlt[3]"
      params_names(60) = "p_res_tech_chg_mlt[4]"
      params_names(61) = "p_serv_cap_out_ratio_1"
      params_names(62) = "p_serv_cap_out_ratio_2"
      params_names(63) = "p_yield_tech_chg_mlt[1]"
      params_names(64) = "p_yield_tech_chg_mlt[2]"
      params_names(65) = "p_yield_tech_chg_mlt[3]"
      params_names(66) = "p_yield_tech_chg_mlt[4]"
      params_names(67) = "perc_food_ratio_init"
      params_names(68) = "pers_pollution_init"
      params_names(69) = "pop1_init"
      params_names(70) = "pop2_init"
      params_names(71) = "pop3_init"
      params_names(72) = "pop4_init"
      params_names(73) = "pot_arable_land_init"
      params_names(74) = "pot_arable_land_tot"
      params_names(75) = "ppoll_in_1970"
      params_names(76) = "ppoll_tech_init"
      params_names(77) = "ppoll_trans_del"
      params_names(78) = "processing_loss"
      params_names(79) = "reproductive_lifetime"
      params_names(80) = "res_tech_init"
      params_names(81) = "service_capital_init"
      params_names(82) = "social_adj_del"
      params_names(83) = "social_discount"
      params_names(84) = "subsist_food_pc"
      params_names(85) = "t_air_poll_time"
      params_names(86) = "t_fcaor_time"
      params_names(87) = "t_fert_cont_eff_time"
      params_names(88) = "t_ind_equil_time"
      params_names(89) = "t_land_life_time"
      params_names(90) = "t_policy_year"
      params_names(91) = "t_pop_equil_time"
      params_names(92) = "t_zero_pop_grow_time"
      params_names(93) = "tech_dev_del_TDD"
      params_names(94) = "urb_ind_land_dev_time"
      params_names(95) = "urban_ind_land_init"
      params_names(96) = "yield_tech_init"

C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine


C--------------- Test06 -----------------
C Optimize Top18 relative with upper and lower boundaries of 1%
      subroutine test06()
      DOUBLE PRECISION params_values(18)
      dimension jbound(18)
      DOUBLE PRECISION bl(18),bu(18),x0(18),wa(657),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test06
        write(*,*) "Inside test06 at date:"
        call system("date")
      params_values = (/ 0.43D0, 3.0D0, 30.0D0, 28.0D0, 3.8D0, 14.0D0,
     *230.0D0, 1.0D0, 12.0D0, 1.0D0, 1000000000000.0D0, 1.0D0,
     *700000000.0D0, 210000000000.0D0, 3200000000.0D0, 20.0D0,
     *2300000000.0D0, 650000000.0D0 /) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 18
      eps=1.d-10
      ibound=1
      do ijbound=1,18
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,18
C Lower bounds: -3% than default
        bl(iparams) = params_values(iparams)*0.97
C Upper bounds: +3% than default
        bu(iparams) = params_values(iparams)*1.03
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test06, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 18)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test06 at date:"
        call system("date")
      end subroutine test06
C Test06: fu
      subroutine fu_test06(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test06!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) =  "p_fioa_cons_const_1"
      params_names(2) =  "p_ind_cap_out_ratio_1"
      params_names(3) =  "reproductive_lifetime"
      params_names(4) =  "life_expect_norm"
      params_names(5) =  "des_compl_fam_size_norm"
      params_names(6) =  "p_avg_life_ind_cap_1"
      params_names(7) =  "subsist_food_pc"
      params_names(8) =  "p_serv_cap_out_ratio_1"
      params_names(9) =  "max_tot_fert_norm"
      params_names(10) = "p_nr_res_use_fact_1"
      params_names(11) = "nr_resources_init"
      params_names(12) = "p_land_yield_fact_1"
      params_names(13) = "pop2_init"
      params_names(14) = "industrial_capital_init"
      params_names(15) = "pot_arable_land_tot"
      params_names(16) = "p_avg_life_serv_cap_1"
      params_names(17) = "pot_arable_land_init"
      params_names(18) = "pop1_init"

C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine


C--------------- Test07 -----------------
C Optimize all the params with no influence curvi 5% bounds
      subroutine test07()
      DOUBLE PRECISION params_values(41)
      dimension jbound(41)
      DOUBLE PRECISION bl(41),bu(41),x0(41),wa(2911),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test07
        write(*,*) "Inside test07 at date:"
        call system("date")

      params_values = (/  2.0D0, 1.2D0, 4800000000.0D0,
     *790000000000.0D0,
     *400.0D0, 2.0D0, 14.0D0, 20.0D0, 0.43D0, 1.0D0, 0.2D0, 0.1D0,
     *0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0, 0.05D0,
     *0.0D0, 0.0D0, 0.0D0, 0.0D0, 0.0D0, 0.0D0, 0.0D0, 0.0D0, 1.0D0,
     *0.0D0, 0.0D0, 0.0D0, 0.0D0, 4000.0D0, 4000.0D0, 4000.0D0,
     *4000.0D0, 4000.0D0, 4000.0D0, 4000.0D0, 4000.0D0 /) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 41
      eps=1.d-10
      ibound=1
      do ijbound=1,41
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,41
C Lower bounds: -3% than default
        bl(iparams) = params_values(iparams)*0.95
C Upper bounds: +3% than default
        bu(iparams) = params_values(iparams)*1.05
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test07, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 41)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test07 at date:"
        call system("date")
      end subroutine test07
C Test07: fu
      subroutine fu_test07(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test07!!!"

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) =  "des_food_ratio_dfr"
      params_names(2) =  "des_ppoll_index_DPOLX"
      params_names(3) =  "des_res_use_rt_DNRUR"
      params_names(4) =  "ind_out_in_1970"
      params_names(5) =  "ind_out_pc_des"
      params_names(6) =  "p_avg_life_agr_inp_2"
      params_names(7) =  "p_avg_life_ind_cap_2"
      params_names(8) =  "p_avg_life_serv_cap_2"
      params_names(9) =  "p_fioa_cons_const_2"
      params_names(10) = "p_fr_cap_al_obt_res_2[1]"
      params_names(11) = "p_fr_cap_al_obt_res_2[2]"
      params_names(12) = "p_fr_cap_al_obt_res_2[3]"
      params_names(13) = "p_fr_cap_al_obt_res_2[4]"
      params_names(14) = "p_fr_cap_al_obt_res_2[5]"
      params_names(15) = "p_fr_cap_al_obt_res_2[6]"
      params_names(16) = "p_fr_cap_al_obt_res_2[7]"
      params_names(17) = "p_fr_cap_al_obt_res_2[8]"
      params_names(18) = "p_fr_cap_al_obt_res_2[9]"
      params_names(19) = "p_fr_cap_al_obt_res_2[10]"
      params_names(20) = "p_fr_cap_al_obt_res_2[11]"
      params_names(21) = "p_ppoll_tech_chg_mlt[1]"
      params_names(22) = "p_ppoll_tech_chg_mlt[2]"
      params_names(23) = "p_ppoll_tech_chg_mlt[3]"
      params_names(24) = "p_ppoll_tech_chg_mlt[4]"
      params_names(25) = "p_res_tech_chg_mlt[1]"
      params_names(26) = "p_res_tech_chg_mlt[2]"
      params_names(27) = "p_res_tech_chg_mlt[3]"
      params_names(28) = "p_res_tech_chg_mlt[4]"
      params_names(29) = "p_serv_cap_out_ratio_2"
      params_names(30) = "p_yield_tech_chg_mlt[1]"
      params_names(31) = "p_yield_tech_chg_mlt[2]"
      params_names(32) = "p_yield_tech_chg_mlt[3]"
      params_names(33) = "p_yield_tech_chg_mlt[4]"
      params_names(34) = "t_air_poll_time"
      params_names(35) = "t_fcaor_time"
      params_names(36) = "t_fert_cont_eff_time"
      params_names(37) = "t_ind_equil_time"
      params_names(38) = "t_land_life_time"
      params_names(39) = "t_policy_year"
      params_names(40) = "t_pop_equil_time"
      params_names(41) = "t_zero_pop_grow_time"

C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine


C--------------- Test08 -----------------
C Optimize Top36 relative with upper and lower boundaries of 3%
      subroutine test08()
      DOUBLE PRECISION params_values(36)
      dimension jbound(36)
      DOUBLE PRECISION bl(36),bu(36),x0(36),wa(2286),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test08
        write(*,*) "Inside test08 at date:"
        call system("date")
      params_values = (/ 0.43D0, 3.0D0, 30.0D0, 28.0D0, 3.8D0, 14.0D0,
     *230.0D0, 1.0D0, 12.0D0, 1.0D0, 1000000000000.0D0, 1.0D0,
     *700000000.0D0, 210000000000.0D0, 3200000000.0D0, 20.0D0,
     *2300000000.0D0, 650000000.0D0, 20.0D0, 0.7D0, 600.0D0, 20.0D0,
     *144000000000.0D0, 900000000.0D0, 1.5D0, 600.0D0, 1.0D0, 1000.0D0,
     *0.001D0, 1.0D0, 136000000.0D0, 0.07D0, 3.0D0, 20.0D0, 20.0D0,
     *0.1D0 /) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 36
      eps=1.d-10
      ibound=1
      do ijbound=1,36
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,36
C Lower bounds: -3% than default
        bl(iparams) = params_values(iparams)*0.97
C Upper bounds: +3% than default
        bu(iparams) = params_values(iparams)*1.03
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test08, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 36)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test08 at date:"
        call system("date")
      end subroutine test08
C Test08: fu
      subroutine fu_test08(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test08!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) =  "p_fioa_cons_const_1"
      params_names(2) =  "p_ind_cap_out_ratio_1"
      params_names(3) =  "reproductive_lifetime"
      params_names(4) =  "life_expect_norm"
      params_names(5) =  "des_compl_fam_size_norm"
      params_names(6) =  "p_avg_life_ind_cap_1"
      params_names(7) =  "subsist_food_pc"
      params_names(8) =  "p_serv_cap_out_ratio_1"
      params_names(9) =  "max_tot_fert_norm"
      params_names(10) = "p_nr_res_use_fact_1"
      params_names(11) = "nr_resources_init"
      params_names(12) = "p_land_yield_fact_1"
      params_names(13) = "pop2_init"
      params_names(14) = "industrial_capital_init"
      params_names(15) = "pot_arable_land_tot"
      params_names(16) = "p_avg_life_serv_cap_1"
      params_names(17) = "pot_arable_land_init"
      params_names(18) = "pop1_init"
      params_names(19) = "ppoll_trans_del"
      params_names(20) = "land_fr_harvested"
      params_names(21) = "inherent_land_fert"
      params_names(22) = "lifet_perc_del"
      params_names(23) = "service_capital_init"
      params_names(24) = "arable_land_init"
      params_names(25) = "assim_half_life_1970"
      params_names(26) = "land_fertility_init"
      params_names(27) = "p_ppoll_gen_fact_1"
      params_names(28) = "avg_life_land_norm"
      params_names(29) = "fr_agr_inp_pers_mtl"
      params_names(30) = "agr_mtl_toxic_index"
      params_names(31) = "ppoll_in_1970"
      params_names(32) = "social_discount"
      params_names(33) = "income_expect_avg_time"
      params_names(34) = "social_adj_del"
      params_names(35) = "hlth_serv_impact_del"
      params_names(36) = "processing_loss"

C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine
C--------------- Test09 -----------------
C Optimize only the "initializers" of the variables that model something from the real life
      subroutine test09()
      DOUBLE PRECISION params_values(17)
      dimension jbound(17)
      DOUBLE PRECISION bl(17),bu(17),x0(17),wa(595),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test09
        write(*,*) "Inside test09 at date:"
        call system("date")
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1
      params_values = (/ 1000000000000.0D0, 700000000.0D0,
     *210000000000.0D0, 3200000000.0D0, 2300000000.0D0, 650000000.0D0,
     *144000000000.0D0, 900000000.0D0, 600.0D0, 136000000.0D0,
     *5000000000.0D0, 8200000.0D0, 190000000.0D0, 60000000.0D0,
     *25000000.0D0, 4800000000.0D0, 790000000000.0D0/) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 17
      eps=1.d-10
      ibound=1
      do ijbound=1,17
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,17
C Lower bounds: -3% than default
        bl(iparams) = params_values(iparams)*0.97
C Upper bounds: +e% than default
        bu(iparams) = params_values(iparams)*1.03
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test09, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 17)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test09 at date:"
        call system("date")
      end subroutine test09
C Test09: fu
      subroutine fu_test09(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test09!!!"

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i":
      params_names(1)  = "nr_resources_init"
      params_names(2)  = "pop2_init"
      params_names(3)  = "industrial_capital_init"
      params_names(4)  = "pot_arable_land_tot"
      params_names(5)  = "pot_arable_land_init"
      params_names(6)  = "pop1_init"
      params_names(7)  = "service_capital_init"
      params_names(8)  = "arable_land_init"
      params_names(9)  = "land_fertility_init"
      params_names(10) = "ppoll_in_1970"
      params_names(11) = "agr_inp_init"
      params_names(12) = "urban_ind_land_init"
      params_names(13) = "pop3_init"
      params_names(14) = "pop4_init"
      params_names(15) = "pers_pollution_init"
      params_names(16) = "des_res_use_rt_DNRUR"
      params_names(17) = "ind_out_in_1970"

C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine
C--------------- Test10 -----------------
C Optimize only the "initializers" of the variables that model something from the real life
      subroutine test10()
      DOUBLE PRECISION params_values(17)
      dimension jbound(17)
      DOUBLE PRECISION bl(17),bu(17),x0(17),wa(595),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test10
        write(*,*) "Inside test10 at date:"
        call system("date")
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1
      params_values = (/ 1000000000000.0D0, 700000000.0D0,
     *210000000000.0D0, 3200000000.0D0, 2300000000.0D0, 650000000.0D0,
     *144000000000.0D0, 900000000.0D0, 600.0D0, 136000000.0D0,
     *5000000000.0D0, 8200000.0D0, 190000000.0D0, 60000000.0D0,
     *25000000.0D0, 4800000000.0D0, 790000000000.0D0/) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 17
      eps=1.d-10
      ibound=1
      do ijbound=1,17
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,17
C Lower bounds: -5% than default
        bl(iparams) = params_values(iparams)*0.95
C Upper bounds: +5% than default
        bu(iparams) = params_values(iparams)*1.05
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test10, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 17)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test10 at date:"
        call system("date")
      end subroutine test10
C Test10: fu
      subroutine fu_test10(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test10!!!"

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i":
      params_names(1)  = "nr_resources_init"
      params_names(2)  = "pop2_init"
      params_names(3)  = "industrial_capital_init"
      params_names(4)  = "pot_arable_land_tot"
      params_names(5)  = "pot_arable_land_init"
      params_names(6)  = "pop1_init"
      params_names(7)  = "service_capital_init"
      params_names(8)  = "arable_land_init"
      params_names(9)  = "land_fertility_init"
      params_names(10) = "ppoll_in_1970"
      params_names(11) = "agr_inp_init"
      params_names(12) = "urban_ind_land_init"
      params_names(13) = "pop3_init"
      params_names(14) = "pop4_init"
      params_names(15) = "pers_pollution_init"
      params_names(16) = "des_res_use_rt_DNRUR"
      params_names(17) = "ind_out_in_1970"

C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine

C--------------- Test11 -----------------
C Similar to test01 but zxpowl instead of curvi
C wa dimensions for zxpowl: n(n+4)

      subroutine test11()
      DOUBLE PRECISION params_values(1)
      DOUBLE PRECISION x0(1),wa(17),fopt,eps  ! CAREFUL! wa from ZXPOWL has a different dimension than wa from curvi
      integer ier
      external fu_test11
      DOUBLE PRECISION fu_test11
        write(*,*) "Inside test11 at date:"
        call system("date")
      params_values = (/1000000000000.0D0/)      !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 1
      eps=1.d-10
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call ZXPOWL(fu_test11,eps,n,x0,fopt,nfu,wa,ier) ! SUBROUTINE ZXPOWL(F,EPS,N,X,FMIN,ITMAX,WA,IER)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)x0(1)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test11 at date:"
        call system("date")
      end subroutine test11
C Test11: fu
      double precision function fu_test11(x)   ! CAREFUL: the function to use in ZXPOWL differs with the one to use in CURVI
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(1), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      integer nvars
      DOUBLE PRECISION x(1)
      DOUBLE PRECISION res_vars_values(1), params_values(1),f


      nvars = 1
      stopTime = 2100
      params_names = (/"nr_resources_init"/)    !careful! you have to change the list length on top if you add or remove a parameter
      target_vars = (/"population"/)
      params_values = x
      nparams = 1
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      fu_test11 = f
      return
      end function

C--------------- Test16 -----------------
C Optimize Top18 relative with upper and lower boundaries of 1%
      subroutine test16()
      DOUBLE PRECISION params_values(18)
      DOUBLE PRECISION x0(18),wa(396),fopt,eps  ! CAREFUL!  the dimensions of wa for zxpowl and for curvi are not the same!
      external fu_test16
      DOUBLE PRECISION fu_test16
      params_values = (/ 0.43D0, 3.0D0, 30.0D0, 28.0D0, 3.8D0, 14.0D0,
     *230.0D0, 1.0D0, 12.0D0, 1.0D0, 1000000000000.0D0, 1.0D0,
     *700000000.0D0, 210000000000.0D0, 3200000000.0D0, 20.0D0,
     *2300000000.0D0, 650000000.0D0 /) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 18
      eps=1.d-10
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call ZXPOWL(fu_test16,eps,n,x0,fopt,nfu,wa,ier) ! SUBROUTINE ZXPOWL(F,EPS,N,X,FMIN,ITMAX,WA,IER)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 18)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
      end subroutine test16
C Test16: fu
      subroutine fu_test16(x)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(18), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(18)
      DOUBLE PRECISION res_vars_values(1), params_values(18),f
      write(*,*) "*** Inside fu_test16!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      nvars = 1
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) =  "p_fioa_cons_const_1"
      params_names(2) =  "p_ind_cap_out_ratio_1"
      params_names(3) =  "reproductive_lifetime"
      params_names(4) =  "life_expect_norm"
      params_names(5) =  "des_compl_fam_size_norm"
      params_names(6) =  "p_avg_life_ind_cap_1"
      params_names(7) =  "subsist_food_pc"
      params_names(8) =  "p_serv_cap_out_ratio_1"
      params_names(9) =  "max_tot_fert_norm"
      params_names(10) = "p_nr_res_use_fact_1"
      params_names(11) = "nr_resources_init"
      params_names(12) = "p_land_yield_fact_1"
      params_names(13) = "pop2_init"
      params_names(14) = "industrial_capital_init"
      params_names(15) = "pot_arable_land_tot"
      params_names(16) = "p_avg_life_serv_cap_1"
      params_names(17) = "pot_arable_land_init"
      params_names(18) = "pop1_init"

C Variable to optimize:
      target_vars = (/"population"/)
      params_values = x
      nparams = 18
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
      f = -res_vars_values(1)
      write(*,*) "f"
      write(*,*) f
      return
      end

C--------------- Test23 -----------------
C Similar to test 03 but "complex" formula using pop and hwi instead of only pop
      subroutine test23()
      DOUBLE PRECISION params_values(12)
      dimension jbound(12)
      DOUBLE PRECISION bl(12),bu(12),x0(12),wa(336),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test23
        write(*,*) "Inside test23 at date:"
        call system("date")
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1
      params_values = (/12.0D0, 0.43D0, 3.0D0, 1.0D0, 28.0D0,
     *3.8D0, 210000000000.0D0, 1.0D0, 1.0D0, 30.0D0, 230.0D0,
     *14.0D0/) !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 12
      eps=1.d-10
      ibound=1
      do ijbound=1,12
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,12
C Lower bounds: -5% than default
        bl(iparams) = params_values(iparams)*0.95
C Upper bounds: +5% than default
        bu(iparams) = params_values(iparams)*1.05
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test23, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 12)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test23 at date:"
        call system("date")
      end subroutine test23
C Test23: fu
      subroutine fu_test23(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(12), target_vars(2)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(2), params_values(n),f
      write(*,*) "*** Inside fu_test23!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

C Last year of the simulation:
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i":
      params_names(1) = "max_tot_fert_norm"
      params_names(2) = "p_fioa_cons_const_1"
      params_names(3) = "p_ind_cap_out_ratio_1"
      params_names(4) = "p_serv_cap_out_ratio_1"
      params_names(5) = "life_expect_norm"
      params_names(6) = "des_compl_fam_size_norm"
      params_names(7) = "industrial_capital_init"
      params_names(8) = "p_land_yield_fact_1"
      params_names(9) = "p_nr_res_use_fact_1"
      params_names(10) = "reproductive_lifetime"
      params_names(11) = "subsist_food_pc"
      params_names(12) = "p_avg_life_ind_cap_1"
C Variables to optimize (or at least receive the output from)
      nvars = 2
      target_vars(1) = "population"
      target_vars(2) = "human_welfare_index"
C Rename for clarification
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
C Formula: -(population/1D10 + human_welfare_index)
      f = -(res_vars_values(1)/1D10 + res_vars_values(2))
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine

C--------------- Test24 -----------------
C Similar to test 04 but "complex" formula using pop and hwi instead of only pop
      subroutine test24()
      DOUBLE PRECISION params_values(12)
      dimension jbound(12)
      DOUBLE PRECISION bl(12),bu(12),x0(12),wa(336),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test24
        write(*,*) "Inside test24 at date:"
        call system("date")
      params_values = (/12.0D0, 0.43D0, 3.0D0, 1.0D0, 28.0D0,
     *3.8D0, 210000000000.0D0, 1.0D0, 1.0D0, 30.0D0, 230.0D0,
     *14.0D0/) !careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 12
      eps=1.d-10
      ibound=1
      do ijbound=1,12
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,12
C Lower bounds: -5% than default
        bl(iparams) = params_values(iparams)*0.97
C Upper bounds: +5% than default
        bu(iparams) = params_values(iparams)*1.03
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test24, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 12)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test24 at date:"
        call system("date")
      end subroutine test24
C Test24: fu
      subroutine fu_test24(n,x,f)
C "Wrapper of the wrapper". Here we set the "parameters" of the
C w3Wrapper (stopTime, params_names,target_vars,nparams)
      CHARACTER*1000 params_names(12), target_vars(2)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(2), params_values(n),f
      write(*,*) "*** Inside fu_test24!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

C Last year of the simulation:
      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i":
      params_names(1) = "max_tot_fert_norm"
      params_names(2) = "p_fioa_cons_const_1"
      params_names(3) = "p_ind_cap_out_ratio_1"
      params_names(4) = "p_serv_cap_out_ratio_1"
      params_names(5) = "life_expect_norm"
      params_names(6) = "des_compl_fam_size_norm"
      params_names(7) = "industrial_capital_init"
      params_names(8) = "p_land_yield_fact_1"
      params_names(9) = "p_nr_res_use_fact_1"
      params_names(10) = "reproductive_lifetime"
      params_names(11) = "subsist_food_pc"
      params_names(12) = "p_avg_life_ind_cap_1"
C Variables to optimize (or at least receive the output from)
      nvars = 2
      target_vars(1) = "population"
      target_vars(2) = "human_welfare_index"
C Rename for clarification
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
C Formula: -(population/1D10 + human_welfare_index)
      f = -(res_vars_values(1)/1D10 + res_vars_values(2))
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine

C--------------- Test26 -----------------
C Similar to test 06 but "complex" formula using pop and hwi instead of only pop
      subroutine test26()
      DOUBLE PRECISION params_values(18)
      dimension jbound(18)
      DOUBLE PRECISION bl(18),bu(18),x0(18),wa(657),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      external fu_test26
        write(*,*) "Inside test26 at date:"
        call system("date")
      params_values = (/ 0.43D0, 3.0D0, 30.0D0, 28.0D0, 3.8D0, 14.0D0,
     *230.0D0, 1.0D0, 12.0D0, 1.0D0, 1000000000000.0D0, 1.0D0,
     *700000000.0D0, 210000000000.0D0, 3200000000.0D0, 20.0D0,
     *2300000000.0D0, 650000000.0D0 /) !careful! the following variables depend on the length of this variable: x1,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 18
      eps=1.d-10
      ibound=1
      do ijbound=1,18
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                        1 if the ith variable has only upper bounds.
c                        2 if the ith variable has only lower bounds.
c                        3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,18
C Lower bounds: -3% than default
        bl(iparams) = params_values(iparams)*0.97
C Upper bounds: +3% than default
        bu(iparams) = params_values(iparams)*1.03
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test26, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 18)
C        write(*,20)x0(1),x0(2)
C20    format(/,2d18.8)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test26 at date:"
        call system("date")
      end subroutine test26
C Test26: fu
      subroutine fu_test26(n,x,f)
      CHARACTER*1000 params_names(n), target_vars(2)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(2), params_values(n),f
      write(*,*) "*** Inside fu_test26!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) =  "p_fioa_cons_const_1"
      params_names(2) =  "p_ind_cap_out_ratio_1"
      params_names(3) =  "reproductive_lifetime"
      params_names(4) =  "life_expect_norm"
      params_names(5) =  "des_compl_fam_size_norm"
      params_names(6) =  "p_avg_life_ind_cap_1"
      params_names(7) =  "subsist_food_pc"
      params_names(8) =  "p_serv_cap_out_ratio_1"
      params_names(9) =  "max_tot_fert_norm"
      params_names(10) = "p_nr_res_use_fact_1"
      params_names(11) = "nr_resources_init"
      params_names(12) = "p_land_yield_fact_1"
      params_names(13) = "pop2_init"
      params_names(14) = "industrial_capital_init"
      params_names(15) = "pot_arable_land_tot"
      params_names(16) = "p_avg_life_serv_cap_1"
      params_names(17) = "pot_arable_land_init"
      params_names(18) = "pop1_init"

C Variables to optimize (or at least receive the output from)
      nvars = 2
      target_vars(1) = "population"
      target_vars(2) = "human_welfare_index"
C Rename for clarification
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
C Formula: -(population/1D10 + human_welfare_index)
      f = -(res_vars_values(1)/1D10 + res_vars_values(2))
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine
C--------------- Test31 -----------------
C Optimize the policy triggers:
C ('t_fert_cont_eff_time', 4000.0, 'Year of continued fertility change')
C ('t_ind_equil_time', 4000.0, 'Year of industrial equilibrium')
C ('t_zero_pop_grow_time', 4000.0, 'Time to zero population growth')
C ('t_land_life_time', 4000.0, 'Land life time')
C ('t_policy_year', 4000.0, 'Year of policy change')
C ('t_fcaor_time', 4000.0, 'Year of capital allocation to resource use efficiency')
      subroutine test31()
      DOUBLE PRECISION params_values(6)
      dimension jbound(6)
      DOUBLE PRECISION bl(6),bu(6),x0(6),wa(132),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      integer pv_I
      external fu_test31
        write(*,*) "Inside test31 at date:"
        call system("date")
      DO pv_I=1,6
        params_values(pv_I) = 2050D0   ! all of the policy triggers default value in the Scenario 1 is 4000, corresponding to year 4000. We need to set a value included in the run or these parameters will have no effect. Therefore, we can't set their default value of 4000
      END DO
!careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 6
      eps=1.d-10
      ibound=1
      do ijbound=1,6
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                             1 if the ith variable has only upper bounds.
c                             2 if the ith variable has only lower bounds.
c                             3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,6
C Lower bounds: fixed at the year 2018
        bl(iparams) = 2018D0
C Upper bounds: fixed at the year 2100
        bu(iparams) = 2100D0
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test31, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 6)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test31 at date:"
        call system("date")
      end subroutine test31
C Test31: fu
      subroutine fu_test31(n,x,f)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test31!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) = "t_fert_cont_eff_time"
      params_names(2) = "t_ind_equil_time"
      params_names(3) = "t_zero_pop_grow_time"
      params_names(4) = "t_land_life_time"
      params_names(5) = "t_policy_year"
      params_names(6) = "t_fcaor_time"
C Variables to optimize (or at least receive the output from)
      nvars = 1
      target_vars(1) = "human_welfare_index"
C Rename for clarification
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
C Formula: -(human_welfare_index)
      f = -(res_vars_values(1))
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine

C--------------- Test32 -----------------
C Optimize the policy triggers:
C ('t_fert_cont_eff_time', 4000.0, 'Year of continued fertility change')
C ('t_ind_equil_time', 4000.0, 'Year of industrial equilibrium')
C ('t_zero_pop_grow_time', 4000.0, 'Time to zero population growth')
C ('t_land_life_time', 4000.0, 'Land life time')
C ('t_policy_year', 4000.0, 'Year of policy change')
C ('t_fcaor_time', 4000.0, 'Year of capital allocation to resource use efficiency')
      subroutine test32()
      DOUBLE PRECISION params_values(6)
      dimension jbound(6)
      DOUBLE PRECISION bl(6),bu(6),x0(6),wa(132),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      integer pv_I
      external fu_test32
        write(*,*) "Inside test32 at date:"
        call system("date")
      DO pv_I=1,6
        params_values(pv_I) = 2018D0   ! all of the policy triggers default value in the Scenario 1 is 4000, corresponding to year 4000. We need to set a value included in the run or these parameters will have no effect. Therefore, we can't set their default value of 4000
      END DO
!careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 6
      eps=1.d-10
      ibound=1
      do ijbound=1,6
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                             1 if the ith variable has only upper bounds.
c                             2 if the ith variable has only lower bounds.
c                             3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,6
C Lower bounds: fixed at the year 2018
        bl(iparams) = 2018D0
C Upper bounds: fixed at the year 2100
        bu(iparams) = 2100D0
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test32, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 6)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test32 at date:"
        call system("date")
      end subroutine test32
C Test32: fu
      subroutine fu_test32(n,x,f)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test32!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) = "t_fert_cont_eff_time"
      params_names(2) = "t_ind_equil_time"
      params_names(3) = "t_zero_pop_grow_time"
      params_names(4) = "t_land_life_time"
      params_names(5) = "t_policy_year"
      params_names(6) = "t_fcaor_time"
C Variables to optimize (or at least receive the output from)
      nvars = 1
      target_vars(1) = "human_welfare_index"
C Rename for clarification
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
C Formula: -(human_welfare_index)
      f = -(res_vars_values(1))
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine

C--------------- Test33 -----------------
C Optimize the policy triggers:
C ('t_fert_cont_eff_time', 4000.0, 'Year of continued fertility change')
C ('t_ind_equil_time', 4000.0, 'Year of industrial equilibrium')
C ('t_zero_pop_grow_time', 4000.0, 'Time to zero population growth')
C ('t_land_life_time', 4000.0, 'Land life time')
C ('t_policy_year', 4000.0, 'Year of policy change')
C ('t_fcaor_time', 4000.0, 'Year of capital allocation to resource use efficiency')
      subroutine test33()
      DOUBLE PRECISION params_values(6)
      dimension jbound(6)
      DOUBLE PRECISION bl(6),bu(6),x0(6),wa(133),fopt,eps  ! don't really know the difference between declaring them as dimension or as double precision
      integer pv_I
      external fu_test33
        write(*,*) "Inside test33 at date:"
        call system("date")
      DO pv_I=1,6
        params_values(pv_I) = 2034D0   ! all of the policy triggers default value in the Scenario 1 is 4000, corresponding to year 4000. We need to set a value included in the run or these parameters will have no effect. Therefore, we can't set their default value of 4000
      END DO
!careful! the following variables depend on the length of this variable: x0,nparams,params_names,n,jbound,bl,bu,wa
      x0 = params_values
      n = 6
      eps=1.d-10
      ibound=1
      do ijbound=1,6
        jbound(ijbound) = 3 ! 0 if the ith variable has no constraints.
c                             1 if the ith variable has only upper bounds.
c                             2 if the ith variable has only lower bounds.
c                             3 if the ith variable has both upper and lower bounds
      end do
      do iparams=1,6
C Lower bounds: fixed at the year 2018
        bl(iparams) = 2018D0
C Upper bounds: fixed at the year 2100
        bu(iparams) = 2100D0
      end do
C BORRAR:
      write(*,*) "params_values"
      write(*,*) params_values

      write(*,*) "bl"
      write(*,*) bl
      write(*,*) "bu"
      write(*,*) bu
C BORRAR^
      nfu=0         ! <--- MAX NUMBER OF CALLS TO FU
      idiff=2
      kmax=3
C IMPORTANT FACT ON wa !!! Read its comment on top

      call curvif(fu_test33, n, x0, fopt, eps, ibound,
     * jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
      write(*,5)ier,nfu,nit
5     format(/,' ier = ',i3,' nfu = ',i5,' nit = ',i6,/)
        write(*,10)
10    format(/,' Vector solucion = ',/)
        write(*,*)(x0(ii), ii = 1, 6)
        write(*,30)fopt
30    format(/,' fopt = ',d18.8,//)
        write(*,*) "Finished test33 at date:"
        call system("date")
      end subroutine test33
C Test33: fu
      subroutine fu_test33(n,x,f)
      CHARACTER*1000 params_names(n), target_vars(1)
      INTEGER stopTime
      INTEGER nparams !careful! this has to correspond to the length of both arrays
      INTEGER nvars
      DOUBLE PRECISION x(n)
      DOUBLE PRECISION res_vars_values(1), params_values(n),f
      write(*,*) "*** Inside fu_test33!!!"
C p_ind_cap_out_ratio_1,3
C p_avg_life_ind_cap_1,14
C p_avg_life_serv_cap_1,20
C p_serv_cap_out_ratio_1,1

      stopTime = 2100
C Parameters names to perturb (the values are set in "test0i"):
C (from most to least influence in Relative 5%)
      params_names(1) = "t_fert_cont_eff_time"
      params_names(2) = "t_ind_equil_time"
      params_names(3) = "t_zero_pop_grow_time"
      params_names(4) = "t_land_life_time"
      params_names(5) = "t_policy_year"
      params_names(6) = "t_fcaor_time"
C Variables to optimize (or at least receive the output from)
      nvars = 1
      target_vars(1) = "human_welfare_index"
C Rename for clarification
      params_values = x
      nparams = n
      call w3Wrapper(stopTime,
     * params_names,params_values,target_vars,nparams,
     * nvars,res_vars_values)
C Formula: -(human_welfare_index)
      f = -(res_vars_values(1))
      write(*,*) "f"
      write(*,*) f
      return
      end subroutine

