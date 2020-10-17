@ECHO OFF
KodPowrotu.exe /S %*

IF %ERRORLEVEL%  GEQ 0 (
  IF %ERRORLEVEL%  LEQ 9 (
    ECHO "Przekazano: prawidlowa wartosc"
  )
)
IF %ERRORLEVEL% == 11 (
ECHO "Brak parametrow"
)
IF %ERRORLEVEL%  == 12 (
ECHO "Parametr %1 nie jest cyfra"
)
IF %ERRORLEVEL% == 13 (
ECHO "Niewlasciwa wartosc parametru" 
)

PAUSE