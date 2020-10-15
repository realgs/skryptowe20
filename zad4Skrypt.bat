@echo off
set /p arg=Wprowadz parametry: 
"KodPowrotu.exe" %arg% /s 


IF %ERRORLEVEL% EQU 11 (
	echo Brak parametrow
	exit /B
)
IF %ERRORLEVEL% EQU 12 (
	echo Parametr %arg% nie jest cyfra
	exit /B
)
IF %ERRORLEVEL% EQU 13 (
	echo Niewlasciwa wartosc parametru %arg%
	exit /B
)

echo Przekazano: prawidlowa wartosc
