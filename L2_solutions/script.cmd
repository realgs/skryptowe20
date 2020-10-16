@ECHO OFF
SET /p param=Podaj parametr:

kodPowrotu.exe /s %param%

IF %ERRORLEVEL%  LEQ 10 (
  ECHO Przekazano: prawidlowa wartosc %ERRORLEVEL%
)
IF %ERRORLEVEL% EQU 11 (
  ECHO Brak parametrow
)

IF %ERRORLEVEL% EQU 12 (
  ECHO Parametr %param% nie jest cyfra
)

IF %ERRORLEVEL% GEQ 13 (
  ECHO Niewlasciwa wartosc parametru %param%
)
