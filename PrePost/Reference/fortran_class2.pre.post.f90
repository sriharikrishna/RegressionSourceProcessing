module OAD_intrinsics
end module
program fClass
  use OAD_active
  use OAD_intrinsics

  TYPE :: POINT
     REAL :: X, Y
  END TYPE POINT
  
  TYPE, EXTENDS(POINT) :: POINT_3D
     REAL :: Z
  END TYPE POINT_3D
  
  TYPE, EXTENDS(POINT) :: COLOR_POINT
     INTEGER :: COLOR
  END TYPE COLOR_POINT
  
  type(POINT),TARGET :: P
  type(POINT_3D),TARGET :: P3
  type(COLOR_POINT),TARGET :: C
  class(POINT),POINTER :: P_OR_C
  
  P_OR_C => C
  SELECT TYPE ( A => P_OR_C )
  CLASS IS ( POINT )
! "CLASS ( POINT ) :: A" implied here
     PRINT *,A%X,A%Y
! This block gets executed
  TYPE IS ( POINT_3D )
! "TYPE ( POINT_3D ) :: A" implied here
     PRINT *,A%X,A%Y,A%Z
  END SELECT
  
end program fClass
