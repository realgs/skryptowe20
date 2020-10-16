@ECHO OFF

set /p arg= Wprowadz parametry:

IF NOT EXIST "KodPowrotu.exe" (
    cl "KodPowrotu.cpp"
)
cmd /c "KodPowrotu.exe" /S %arg%

IF NOT ERRORLEVEL 10 (
	Echo Przekazano: prawidlowa wartosc
)
IF %ERRORLEVEL% EQU 11 (
	Echo Brak parametrow
)
IF %ERRORLEVEL% EQU 12 (
	Echo Parametr %arg% nie jest cyfra
)
IF %ERRORLEVEL% EQU 13 (
	Echo Niewlasciwa wartosc parametru %arg%
)
PAUSE