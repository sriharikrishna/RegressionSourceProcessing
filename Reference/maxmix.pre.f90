module OAD_intrinsics
  interface oad_s_max
    module procedure oad_s_max_r,oad_s_max_d
  end interface
  contains
    subroutine oad_s_max_r(a,b,r)
      real,intent(in) :: a
      real,intent(in) :: b
      real,intent(out) :: r
      if (a>b) then
        r = a
      else
        r = b
      end if
    end subroutine
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
program p
  use OAD_intrinsics
  implicit none
  double precision :: d
  real :: r
  integer :: i
  real :: oad_ctmp0
  double precision :: oad_ctmp1
  i = 2
  r = 2.0
  d = 2.0D0
  i = max(i,3)
  call oad_s_max(r,2.5,oad_ctmp0)
  r = oad_ctmp0
  call oad_s_max(d,2.5D0,oad_ctmp1)
  d = oad_ctmp1
end program

