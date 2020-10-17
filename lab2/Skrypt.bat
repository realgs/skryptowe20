@echo off
KodPowrotu\KodPowrotu\KodPowrotu.exe %* /s

IF %ERRORLEVEL% LEQ 9 (
	ECHO Przekazano prawidlowa wartosc
)

IF %ERRORLEVEL% == 11 (
    ECHO Nie podano parametrow
) 
IF %ERRORLEVEL% == 12 (
    ECHO Parametr nie jest liczba
)

IF %ERRORLEVEL% == 13 (
   ECHO Niewlasciwa ilosc parametrow
) 