program maxDouble
  double precision :: x
  integer :: i
  x = 3.D0
  if (x>2.0D0) then
    x = x-1.0D0
  endif ! c endif
  do i = 1,2,1
    x = x+1.0
  enddo ! c enddo
  write(*,*) 'x = ',x
end program maxDouble