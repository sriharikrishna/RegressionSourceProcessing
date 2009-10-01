    program functionComment
      real :: x

      x = 1.5D0
      print *,f(x)
    end program functionComment

    function f(x)
      real :: x,f

      f = 5
    end function f

    subroutine oad_s_f(x,f)
      real,intent(out) :: f
      real :: x

      f = 5
    end subroutine oad_s_f

