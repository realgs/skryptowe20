#!/bin/bash

PRODUKT1=$1
PRODUKT2=$2
DATA=$3

less ./zakup.txt | ./StarczyJeden "$PRODUKT1" | ./SelKol 3 | ./SumaNum
less ./zakup.txt | ./StarczyJeden "$PRODUKT1" "$PRODUKT2" | ./SelKol 3 | ./SumaNum
less ./zakup.txt | ./StarczyJeden "$DATA" | ./SelKol 2 | sort
less ./zakup.txt | ./StarczyJeden "$DATA" | ./SelKol 4 | ./SumaNum
