subroutine curvif_simplified(x0, obj_func, x_opt, f_opt, n)
    ! Declarations
    implicit none
    double precision :: obj_func, fopt_tmp
    integer, intent(in) :: n
    double precision, intent(in) :: x0(n)
    double precision, intent(out) :: f_opt, x_opt(n)
    integer :: i
    external obj_func
    ! Instructions
    do i = 1, n
        x_opt(i) = x0(i)+1
        fopt_tmp = obj_func(x0,n)
    end do
    f_opt = 23
end
