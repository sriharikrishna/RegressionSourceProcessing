module OAD_intrinsics
end module
MODULE m
use OAD_active
use OAD_intrinsics
PRIVATE
PUBLIC :: foo
public :: oad_s_foo

CONTAINS

FUNCTION foo(i) RESULT(status)
        INTEGER i
        INTEGER status
        status=1
        return
END FUNCtion

subroutine oad_s_foo(i,status)
        INTEGER i
        integer,intent(out) :: status
        status=1
        return
end subroutine oad_s_foo

end module

program p
use OAD_active
use OAD_intrinsics
use m
  integer :: oad_ctmp0
  integer :: oad_ctmp1
i=2
oad_ctmp1 = i
call oad_s_foo(oad_ctmp1,oad_ctmp0)
j = oad_ctmp0
end
