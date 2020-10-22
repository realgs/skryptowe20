produkt="produkt"
produkt1="produkt1"
produkt2="produkt2"
dzien="11.08.2010"

echo "4.1.)"
cat Zakup.txt | python3 SelKol.py 1 2 3| python3 StarczyJeden.py $produkt | python3 SumaNum.py;
echo "4.2.)"
cat Zakup.txt | python3 SelKol.py 1 2 3| python3 StarczyJeden.py $produkt1 $produkt2 | python3 SumaNum.py;
echo "4.3.)"
cat Zakup.txt | python3 StarczyJeden.py $dzien | python3 SelKol.py 2| sort
echo "4.4.)"
cat Zakup.txt | python3 StarczyJeden.py $dzien | python3 SelKol.py 4 | python3 SumaNum.py;
