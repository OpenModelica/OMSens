subroutine curvif_simplified(x0, obj_func, lower_bounds, upper_bounds, epsilon, n, x_opt, f_opt)
    ! Declarations
    implicit none
    integer, intent(in) :: n
    double precision :: epsilon, wa(9*n+n*(n+1)/2+n*n+max(7*n-n*(n+1)/2,0))
!    double precision :: fopt_tmp
    double precision, intent(in) :: x0(n), lower_bounds(n), upper_bounds(n)
    double precision, intent(out) :: f_opt, x_opt(n)
    integer :: i, ibound, nfu, idiff, kmax, jbound(n), nit, ier
    external obj_func, curvif

    ! Initialize CURVI inputs that are used with the same value for every test
!    epsilon=1.d-10! tolerance for the stopping criterion.
    ibound=1      ! 1 if constrained problem
    nfu=0         ! max number of calls to fu
    idiff=2       ! idiff = 2  central differences
    kmax=3        ! hessian is recomputed after kmax iterations
    DO i=1,n
        jbound(i)=3      ! 3 if the ith variable has both upper and lower bounds
    end do
    call curvif(obj_func, &
     n,                   &
     x0,                  &
     f_opt,               &
     epsilon,             &
     ibound,              &
     jbound,              &
     lower_bounds,        &
     upper_bounds,        &
     wa,                  &
     nfu,                 &
     nit,                 &
     idiff,               &
     kmax,                &
     ier)
    do i = 1, n
        x_opt(i) = x0(i)
    end do
end
