program maxDouble
  implicit none ! c1
  double precision x,y ! c2
  double precision :: oad_ctmp0
! ! c3
  x = 3.1415D0
  call oad_s_max_d(x,8.90D0,oad_ctmp0)
  y = oad_ctmp0
  write(*,*) 'y = ',y
end program maxDouble !c7
subroutine oad_s_max_d(a,b,r)
  double precision,intent(in) :: a
  double precision,intent(in) :: b
  double precision,intent(out) :: r
  if (a>b) then
    r = a
  else
    r = b
  endif
end
