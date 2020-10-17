@echo off

KodPowrotu\KodPowrotu\KodPowrotu.exe %* /s

IF %ERRORLEVEL% LEQ 9 (
	ECHO Przekazano prawidlowa wartosc

IF %ERRORLEVEL% EQU 11 (
	ECHO Brak Parametrow
)

IF %ERRORLEVEL% EQU 12 (
    ECHO Parametr nie jest liczba
)

IF %ERRORLEVEL% EQU 13 (
   ECHO Niewlasciwa ilosc parametrow
) 