module OAD_intrinsics
end module
subroutine foo(x)
use OAD_intrinsics
use OAD_active
double precision x
print *,x
end subroutine

program p
use OAD_intrinsics
use OAD_active
implicit real (q)
implicit real*8 (p)
implicit double precision (i-m)
  double precision :: oad_ctmp0
j=3
oad_ctmp0 = j+5
call foo(oad_ctmp0)
end program
