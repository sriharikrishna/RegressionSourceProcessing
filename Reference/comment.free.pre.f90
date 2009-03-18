program maxDouble ! c0
  implicit none ! c1
  double precision x,y ! c2
  double precision :: oad_ctmp0
  ! c3
  x = 3.1415  ! c4
  call oad_s_max_d(x,8.90,oad_ctmp0)
  y = oad_ctmp0
  write(*,*) 'y = ',y ! c6 
end program maxDouble !c7

