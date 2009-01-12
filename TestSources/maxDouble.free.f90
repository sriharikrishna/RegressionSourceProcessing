SUBROUTINE oad_s_max_d(FIRST, SECOND, RESULT)
  implicit none
  double precision :: FIRST,SECOND,RESULT

  write(*,*) 'second = ',SECOND

  IF(FIRST .LT. SECOND) THEN
    RESULT = SECOND
  ELSE
    RESULT = FIRST
  ENDIF
END SUBROUTINE

program nested
  implicit none
  double precision x,y

  x = 3.1415
  y = max(x,8.90)
  write(*,*) 'y = ',y
end program nested

