module OAD_intrinsics
end module
program anyTest
use OAD_intrinsics
use OAD_active
   real :: X(2)

   X = 1.0
   if (any(x(1:2)/=0.0)==.true.) then
     print *,'OK'
   end if
end program
 
