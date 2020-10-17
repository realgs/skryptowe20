@echo off

CMD /c "return_code.exe" /s %*

IF %errorlevel% EQU 11 (
    ECHO Brak parametrow
) ELSE IF %errorlevel% EQU 12 (
    ECHO Parametr/y nie sa cyfra
) ELSE IF %errorlevel% EQU 13 (
    ECHO Niewlasciwa wartosc parametru
) ELSE (
    ECHO Przekazano prawidlowy parametr
)
