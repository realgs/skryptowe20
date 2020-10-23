@ECHO OFF

set /p day= Insert day:

echo.
cmd /c "StarczyJeden.exe" %day% < Zakup.txt | SelKol.exe 4 | "SumaNum.exe"