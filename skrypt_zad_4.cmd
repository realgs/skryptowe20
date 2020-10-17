@echo off

SET params=%*
KodPowrotu.exe /S %params%

IF %errorlevel% == 11 (
    ECHO  Brak parametrow
) ELSE IF %errorlevel% == 12 (
    ECHO Parametr %params% nie jest cyfra
) ELSE IF %errorlevel% == 13 (
    ECHO Niewlasciwa wartosc parametru %params%
) ELSE (
    ECHO Przekazano: %params%
)
 