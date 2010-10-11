module OAD_intrinsics
end module
module m
contains
subroutine foo(x)
use OAD_intrinsics
use OAD_active
implicit double precision (x)
print *,x
end subroutine
subroutine bar(x)
use OAD_intrinsics
use OAD_active
implicit none
double precision x
print *,x
end subroutine
end module

program p
use OAD_intrinsics
use OAD_active
use m
implicit none
double precision j
  double precision :: oad_ctmp0
j=3
oad_ctmp0 = j+5
call foo(oad_ctmp0)
end program
