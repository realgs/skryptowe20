@ECHO OFF

"./KodPowrotu.exe"  %* /s

IF %ERRORLEVEL% EQU 11 (
	ECHO Brak parametrow
	EXIT /B
)
IF %ERRORLEVEL% EQU 12 (
	ECHO Parametr %* nie jest cyfra
	EXIT /B
)
IF %ERRORLEVEL% EQU 13 (
	ECHO Niewlasciwa wartosc parametru %*
	EXIT /B
)

ECHO Przekazano: %1
