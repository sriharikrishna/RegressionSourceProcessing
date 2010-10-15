module OAD_intrinsics
end module
program p
use OAD_intrinsics
use OAD_active
implicit none
dimension a(3)
real a
data a /.1,.2,.3/
print *,a
end
