@echo off
type Zakup.txt | python SelKol.py 1 2 3 | python StarczyJeden.py %1 %2 | python SumaNum.py
