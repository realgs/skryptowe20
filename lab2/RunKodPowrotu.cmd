@ECHO OFF

KodPowrotu.exe /s %*

IF %ERRORLEVEL% LSS 10 (
    ECHO Przekazano: prawidlowa wartosc
) ELSE IF %ERRORLEVEL% EQU 11 (
    ECHO Brak parametrow
) ELSE IF %ERRORLEVEL% EQU 12 (
    ECHO Parametr %* nie jest cyfra
) ELSE IF %ERRORLEVEL% EQU 13 (
    ECHO Niewlasciwa wartosc parametru %*
)
