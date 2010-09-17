module OAD_intrinsics
end module
program maxDouble
use OAD_intrinsics
use OAD_active
  double precision x
  integer i
  x = 3.D0
  if (x>2.0D0) then
    x = x-1.0D0
  endif
  do i=1,2,1
    x = x+1.0
  enddo
  write(*,*) 'x = ',x
end program maxDouble

