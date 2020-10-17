@ECHO OFF

SET params=%*

KodPowrotu.exe /s %params%

IF %ERRORLEVEL% LEQ 10 ECHO Przekazano: prawidlowa wartosc
IF %ERRORLEVEL% EQU 11 ECHO Brak parametrow
IF %ERRORLEVEL% EQU 12 ECHO Parametr %params% nie jest cyfra
IF %ERRORLEVEL% EQU 13 ECHO Niewlasciwa wartosc parametru %params%