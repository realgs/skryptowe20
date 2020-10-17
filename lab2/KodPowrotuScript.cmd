@echo off

KodPowrotu.exe %* /s

SET returnValue=%ERRORLEVEL%

IF %returnValue% EQU 11 (
	ECHO Brak parametrow
)ELSE (
	IF %returnValue% EQU 12 (
		ECHO Parametr X nie jest cyfra
	)ELSE (
		IF %returnValue% EQU 13 (
			ECHO Zbyt wiele parametrow
		)ELSE (
			ECHO Przekazano: prawidlowa wartosc
		)
	)
)
