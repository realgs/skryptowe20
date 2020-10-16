@ECHO OFF

SET script_params=%*

kodPowrotu.exe /s %script_params%

IF %ERRORLEVEL%  LEQ 10 (
  ECHO Przekazano: prawidlowa wartosc

) ELSE IF %ERRORLEVEL% EQU 11 (
  ECHO Brak parametrow

) ELSE IF %ERRORLEVEL% EQU 12 (
  ECHO Parametr %script_params% nie jest cyfra

) ELSE IF %ERRORLEVEL% EQU 13 (
  ECHO Niewlasciwa wartosc parametru %script_params%
) 
