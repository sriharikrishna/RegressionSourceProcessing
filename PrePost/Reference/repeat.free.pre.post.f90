module OAD_intrinsics
end module
subroutine foo(xxx)
use OAD_intrinsics
use OAD_active
  character :: xxx(3)
  print *,xxx
end subroutine

program p
use OAD_intrinsics
use OAD_active
  character :: xxx(3),x
  x='x'
  call foo(repeat(x,3))
end program
  
