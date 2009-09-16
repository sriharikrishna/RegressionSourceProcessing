module m

  interface erf
    module procedure real_erf, double_erf
  end interface

  interface erfc
    module procedure real_erfc, double_erfc
  end interface

  contains

    real function real_erf (z) result (zr)
      real :: z
      zr = z*4.3E0
    end function real_erf

    double precision function double_erf (z) result (zr)
      double precision :: z
      zr = z*5.0D0
    end function double_erf

    real function real_erfc (z) result (zr)
      real :: z
      zr = z*7.0E0
    end function real_erfc

    double precision function double_erfc (z) result (zr)
      double precision :: z
      zr = z*3.0D0
    end function double_erfc

end module m

program multipleModuleProcedures
  use m
  implicit none
  real :: a
  double precision :: b
  real :: oad_ctmp0
  real :: oad_ctmp1
  double precision :: oad_ctmp2
  double precision :: oad_ctmp3

  call oad_s_real_erf(1.0E0,oad_ctmp0)
  call oad_s_real_erfc(2.0E0,oad_ctmp1)
  a = oad_ctmp0+oad_ctmp1
  call oad_s_double_erf(1.0D0,oad_ctmp2)
  call oad_s_double_erfc(2.0D0,oad_ctmp3)
  b = oad_ctmp2+oad_ctmp3
  print *,a,' ',b
end program multipleModuleProcedures
