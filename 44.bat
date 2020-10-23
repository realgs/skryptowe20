@echo off
type Zakup.txt | python StarczyJeden.py %1 | python SelKol.py 4 | python SumaNum.py
