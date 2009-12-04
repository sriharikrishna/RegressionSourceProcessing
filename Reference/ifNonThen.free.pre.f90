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
program ifNonThen
  use OAD_intrinsics
  implicit none
  double precision x,y
  double precision :: oad_ctmp0
  double precision :: oad_ctmp1

  x = 3.1415D0
  call oad_s_max(x,8.90D0,oad_ctmp0)
  if (x.le.oad_ctmp0) then
    call oad_s_max(x,8.90D0,oad_ctmp1)
    y = oad_ctmp1
  end if
  write(*,*) 'y = ',y
end program ifNonThen

