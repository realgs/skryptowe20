@ECHO OFF

KodPowrotu.exe /S %*

IF %ERRORLEVEL% EQU 11 (
    Echo Brak parametrów 
) ELSE IF %ERRORLEVEL% EQU 12 ( 
    Echo Parametr %* nie jest cyfrą 
) ELSE IF %ERRORLEVEL% EQU 13 (
    Echo Niewłaściwa wartość parametru %* 
) ELSE ( 
    Echo Przekazano: %ERRORLEVEL% 
)
