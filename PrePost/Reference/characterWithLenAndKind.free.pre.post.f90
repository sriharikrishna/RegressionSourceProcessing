module OAD_intrinsics
end module
program p
use OAD_intrinsics
use OAD_active
  character(kind=kind('A'), len=10) :: name
  name='blah'
  print *,name
end program
