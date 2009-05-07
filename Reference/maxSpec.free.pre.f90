program maxSpec
  implicit none
  double precision x,y
  double precision :: oad_ctmp0

  x = 3.1415D0
  call oad_s_max_d(x,8.90D0,oad_ctmp0)
  y = oad_ctmp0
  write(*,*) 'y = ',y
end program 

