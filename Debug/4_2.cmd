@ECHO OFF

set /p product1= Insert product 1 name:
set /p product2= Insert product 2 name:

echo.
cmd /c "StarczyJeden.exe" %product1% %product2% < Zakup.txt | "SelKol.exe" 3 | "SumaNum.exe"