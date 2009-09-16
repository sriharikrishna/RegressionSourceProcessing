module psget_I
  interface
    real(KIND(0.0D0)) function psget(I)
      integer,INTENT(IN) :: I
    END FUNCTION psget
  end interface
END MODULE
program interfaceSymtab
  use psget_I
use OAD_active
  integer :: i

  i = 1
  print *,'i = ',i
end program interfaceSymtab
