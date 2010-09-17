module OAD_intrinsics
end module
program alogTest
use OAD_intrinsics
use OAD_active
   real :: Y,X

   X = 1
   Y = log(X)
   print *,Y

end program alogTest
 
