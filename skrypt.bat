@ECHO OFF

C:\Users\Patrycja\Documents\Git\lab2\lab2\Debug\lab2.exe /s %*
IF %ERRORLEVEL% EQU 11 ECHO Brak parametrow
IF %ERRORLEVEL% EQU 12 ECHO Parametr %1 nie jest cyfra
IF %ERRORLEVEL% EQU 13 ECHO Niewlasciwa liczba parametrow
IF %ERRORLEVEL% LSS 10 IF %ERRORLEVEL% GEQ 0 ECHO Przekazano: prawidlowa wartosc