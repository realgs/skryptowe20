@ECHO OFF
KodPowrotu.exe %* /s

IF %ERRORLEVEL% == 11 (
    ECHO Nie podano parametrow
) ELSE IF %ERRORLEVEL% == 12 (
    ECHO Parametr nie jest liczba
) ELSE IF %ERRORLEVEL% == 13 (
   ECHO Niewlasciwa ilosc parametrow
) ELSE (
    ECHO Przekazano prawidlowa wartosc
)