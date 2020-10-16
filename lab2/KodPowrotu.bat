@echo OFF

set /p parametr=Podaj parametr KodPowrotu:

KodPowrotu.exe \s %parametr%
IF %ERRORLEVEL% EQU 11 ECHO Brak parametrow
IF %ERRORLEVEL% EQU 12 ECHO Parametr %parametr% nie jest cyfra
IF %ERRORLEVEL% EQU 13 ECHO Niewlasciwa liczba parametrow
IF %ERRORLEVEL% LSS 10 ECHO Przekazano: prawidlowa wartosc