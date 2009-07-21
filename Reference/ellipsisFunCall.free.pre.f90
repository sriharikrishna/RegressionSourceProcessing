program p
  real :: u=1.0,v=1.1,w=1.2,x=0.9,y=0.8,z
  real :: oad_ctmp0
  real :: oad_ctmp1
  real :: oad_ctmp2
  real :: oad_ctmp3
  real :: oad_ctmp4
  call oad_s_max_r(x,y,oad_ctmp4)
  call oad_s_max_r(w,oad_ctmp4,oad_ctmp3)
  call oad_s_max_r(v,oad_ctmp3,oad_ctmp2)
  call oad_s_max_r(u,oad_ctmp2,oad_ctmp1)
  z = oad_ctmp1
  print *,z
end program
subroutine oad_s_max_r(a,b,r)
  real,intent(in) :: a
  real,intent(in) :: b
  real,intent(out) :: r
  if (a>b) then
    r = a
  else
    r = b
  endif
end
