@ECHO OFF
SET /p param=Podaj parametr:

CMD /c "kodPowrotu.exe" /s %param%

IF %ERRORLEVEL%  LEQ 10 (
  echo Przekazano: prawidlowa wartosc %ERRORLEVEL%
)
IF %ERRORLEVEL% EQU 11 (
  echo Brak parametrow
)

IF %ERRORLEVEL% EQU 12 (
  echo Parametr %param% nie jest cyfra
)

IF %ERRORLEVEL% EQU 13 (
  echo Niewlasciwa wartosc parametru %param%
)
