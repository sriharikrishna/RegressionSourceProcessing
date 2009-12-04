module OAD_intrinsics
  interface oad_s_max
    module procedure oad_s_max_d
  end interface
  contains
    subroutine oad_s_max_d(a,b,r)
      double precision,intent(in) :: a
      double precision,intent(in) :: b
      double precision,intent(out) :: r
      if (a>b) then
        r = a
      else
        r = b
      end if
    end subroutine
end module
program maxDouble
  use OAD_intrinsics
use OAD_active
  implicit none
  double precision x,y
  double precision :: oad_ctmp0
! c3
  x = 3.1415D0
  call oad_s_max(x,8.90D0,oad_ctmp0)
  y = oad_ctmp0
  write(*,*) 'y = ',y
end program maxDouble

