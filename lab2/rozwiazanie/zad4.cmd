@ECHO OFF
cmd /c "KodPowrotu.exe" /s %*
IF %ERRORLEVEL% EQU 11 (
    Echo Brak parametrow
) ELSE ( IF %ERRORLEVEL% EQU 12 (
            Echo Parametr %1 nie jest cyfra
        ) ELSE ( IF %ERRORLEVEL% EQU 13 (
                Echo Niewlasciwa wartosc parametru %arg%
                ) ELSE (
                        Echo Przekazano: %1
)
) 
) 
