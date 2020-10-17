@ECHO OFF

SET parameters=%*

KodPowrotu.exe /s %parameters%

IF %ERRORLEVEL% GEQ 0 IF %ERRORLEVEL% LSS 10 (
  ECHO Przekazano: prawidlowa wartosc %parameters%
  
) ELSE IF %ERRORLEVEL% EQU 11 (
  ECHO Brak parametrow

) ELSE IF %ERRORLEVEL% EQU 12 (
  ECHO Parametr %parameters% nie jest cyfra

) ELSE IF %ERRORLEVEL% EQU 13 (
  ECHO Niewlasciwa wartosc parametru %parameters%
)
