@echo off
set /p parameter=Wprowadz parametry programu "KodPowrotu":
KodPowrotu.exe /s %parameter%

IF %ERRORLEVEL% EQU 11 (
	echo Brak parametrow
	pause
	exit /B
)

IF %ERRORLEVEL% EQU 12 (
	echo Parametr %parameter% nie jest cyfra
	pause
	exit /B
)

IF %ERRORLEVEL% EQU 13 (
	echo Niewlasciwa wartosc parametru %parameter%
	pause
	exit /B
)

echo Przekazano: %parameter%
pause
exit /B 