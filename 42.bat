@echo off
type Zakup.txt | python StarczyJeden.py %1 %2 | python SelKol.py 3  | python SumaNum.py
