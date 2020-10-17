@ECHO OFF

cd ..

ECHO Test programu dla poprawnej wartosci (bez /s):
KodPowrotu.exe 7
ECHO ERRORLEVEL = %ERRORLEVEL%

ECHO Test programu dla poprawnej wartosci (z /s):
KodPowrotu.exe 2 /s
ECHO ERRORLEVEL = %ERRORLEVEL%

ECHO Test programu dla braku parametrow (bez /s):
KodPowrotu.exe 
ECHO ERRORLEVEL = %ERRORLEVEL%

ECHO Test programu dla braku parametrow (z /s):
KodPowrotu.exe /S
ECHO ERRORLEVEL = %ERRORLEVEL%

ECHO Test programu dla zbyt wielu parametrow (bez /s):
KodPowrotu.exe 1caev 5
ECHO ERRORLEVEL = %ERRORLEVEL%

ECHO Test programu dla zbyt wielu parametrow (z /s):
KodPowrotu.exe 1 4 5 /s
ECHO ERRORLEVEL = %ERRORLEVEL%

ECHO Test programu dla niepoprawnej wartosci parametru (bez /s):
KodPowrotu.exe 12
ECHO ERRORLEVEL = %ERRORLEVEL%

ECHO Test programu dla niepoprawnej wartosci parametru (z /s):
KodPowrotu.exe awf /s
ECHO ERRORLEVEL = %ERRORLEVEL%

cd tests
