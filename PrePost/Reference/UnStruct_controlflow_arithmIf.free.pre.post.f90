module OAD_intrinsics
end module
program p
use OAD_intrinsics
use OAD_active
integer i
i=2
if (i-3) 10,20,10
goto 50
 10            print *,'10'
goto 50
 20            print *,'20'
 50            continue
end