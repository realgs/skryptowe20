@echo off
more Zakup.txt | python StarczyJeden.py %1 | python SelKol.py 2 | sort
