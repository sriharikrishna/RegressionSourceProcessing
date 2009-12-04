module OAD_intrinsics
end module
    program functionComment
use OAD_intrinsics
    use OAD_active
      real :: x

      x = 1.5D0
      print *,f(x)
    end program functionComment

    function f(x)
use OAD_intrinsics
    use OAD_active
      real :: x,f

      f = 5
    end function f

    subroutine oad_s_f(x,f)
use OAD_intrinsics
    use OAD_active
      real,intent(out) :: f
      real :: x

      f = 5
    end subroutine oad_s_f
