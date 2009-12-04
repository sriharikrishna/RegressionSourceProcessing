module OAD_intrinsics
end module
    program functionComment
use OAD_intrinsics
      real :: x

      x = 1.5D0
      print *,f(x)
    end program functionComment

    function f(x)
use OAD_intrinsics
      real :: x,f

      f = 5
    end function f

    subroutine oad_s_f(x,f)
use OAD_intrinsics
      real,intent(out) :: f
      real :: x

      f = 5
    end subroutine oad_s_f
