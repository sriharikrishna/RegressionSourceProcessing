module OAD_intrinsics
end module
subroutine s1()
  real :: x
  contains
  real function foo(x)
  use OAD_intrinsics
    integer:: x
    foo=x
  end function
  subroutine oad_s_foo(x,foo)
  use OAD_intrinsics
    integer:: x
    real,intent(out) :: foo
    foo=x
  end subroutine oad_s_foo
end subroutine

subroutine s2()
  real :: x
  contains
  real function foo(x)
  use OAD_intrinsics
   integer :: x
   foo=x
  end function
  subroutine oad_s_foo(x,foo)
  use OAD_intrinsics
   integer :: x
   real,intent(out) :: foo
   foo=x
  end subroutine oad_s_foo
end subroutine

program p
use OAD_intrinsics
  call s1
  call s2
end program
