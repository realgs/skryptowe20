@ECHO OFF

set /p product= Insert product name:

echo.
cmd /c "StarczyJeden.exe" %product% < Zakup.txt | "SelKol.exe" 3 | "SumaNum.exe"
