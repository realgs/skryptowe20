@echo off

IF NOT EXIST KodPowrotu.exe (
    ECHO Plik KodPowrotu.exe nie zostal znaleziony
    EXIT /b
)

KodPowrotu.exe /s %*

IF %errorlevel% EQU 11 (
    ECHO Brak parametru
) ELSE IF %errorlevel% EQU 12 (
    ECHO Parametr %* nie jest cyfra
) ELSE IF %errorlevel% EQU 13 (
    ECHO Niewlasciwa wartosc parametru: %*
) ELSE (
    ECHO Przekazano: %errorlevel%
)

