@ECHO OFF

echo.
cmd /c "StarczyJeden.exe" %1% < Zakup.txt | "SelKol.exe" 3 | "SumaNum.exe"
