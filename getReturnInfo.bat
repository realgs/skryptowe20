set /p param=Wpisz parametry programu:
KodPowrotu.exe /s %param%

IF %ERRORLEVEL% EQU 11 (
	echo Brak parametrow
	pause
	exit /B
)

IF %ERRORLEVEL% EQU 12 (
	echo Parametr %param% nie jest cyfra
	pause
	exit /B
)

IF %ERRORLEVEL% EQU 13 (
	echo Niewlasciwa wartosc parametru %param%
	pause
	exit /B
)

echo Przekazano: %param%
pause
exit /B