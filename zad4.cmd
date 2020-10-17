@echo off
start "." /wait Z1.exe %* /s
if %errorlevel% equ 11 (
    echo Brak parametrow
) else if %errorlevel% equ 12 (
    echo Parametr %1 nie jest cyfra
) else if %errorlevel% equ 13 (
    echo Zla liczba argumentow
) else (
    echo Przekazano: prawidlowa wartosc %1
)