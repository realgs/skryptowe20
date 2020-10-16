@echo off
ReturnCode /S %*

IF %errorlevel% EQU 13 (
    ECHO Niewłaściwa ilość parametrów
) ELSE IF %errorlevel% EQU 12 (
    ECHO Parametr nie jest liczbą
) ELSE IF %errorlevel% EQU 11 (
    ECHO Nie podano parametrów
) ELSE (
    ECHO Przekazano prawidłową wartość
)