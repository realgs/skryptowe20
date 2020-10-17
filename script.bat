@echo off

IF NOT EXIST KodPowrotu.exe (
	echo Brak pliku KodPowrotu.exe
	EXIT /b
)

KodPowrotu /s %*

IF %errorlevel% EQU 13 (
	ECHO Niewlasciwa wartosc parametru: %*
) ELSE IF %errorlevel% EQU 12 (
	ECHO Parametr %* nie jest cyfra
) ELSE IF %errorlevel% EQU 11 (
	ECHO Brak parametru
) ELSE (
	ECHO Przekazana: %errorlevel%
)

