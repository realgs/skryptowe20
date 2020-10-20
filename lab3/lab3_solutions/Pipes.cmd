@echo off

set /p product1= Insert product1 name:
set /p produkt2= Insert produkt2 name:
set /p day= Day Insert:
set /a value_column_id = 3

echo.
cmd /c "StarczyJeden.exe" %product1% < Zakup.txt | "SelKol.exe" 2 | "SumaNum.exe"

echo.
cmd /c "StarczyJeden.exe" %product1% %produkt2% < Zakup.txt | "SelKol.exe" 2 | "SumaNum.exe"

echo.
cmd /c "StarczyJeden.exe" %day% < Zakup.txt | sort

echo.
cmd /c "StarczyJeden.exe" %day% < Zakup.txt | SelKol.exe %value_column_id% | "SumaNum.exe"