1. Uruchomienie 
Żeby uruchomić program należy posiadać na komputerze Pythona w wersji 3 oraz dodatki do niego, takie jak:
-django
-sqlite3
-request
Należy również posiadać odpowiednią bazę danych, z której korzysta program.

Projekt był tworzony w pyCharm (używając Anacondy), więc jest on ułożony w katalogi. Uruchamia się go korzystając z terminala
i wpisując komendę: python manage.py runserver. Otrzymujemy wtedy link do naszego API. Należy w niego wejść.

2.Pobieranie danych
Żeby pobrać kursy danej waluty z ostatnich kilu dni należy dopisać po / do url naszego api następujące rzeczy:
-/waluta - pobierzemy ostatnie notowanie waluty wpisanej po /. Należy wpisać skrót 3 literowy, np. USD, PLN, EUR.
-/waluta/last/dni - pobierzemy notowanie waluty wpisanej po pierwszym / z ostatnich dni(liczba) wpisanych po / po last, np. usd/last/30.
-/sales/from/data - pobierzemy łączą sumę sprzedaży z podanej daty (format yyyy-mm-dd) z bazy danych sprzedaży, np./2015-01-01.
Gdyby podana waluta była nieobsługiwana, dostaniemy komunikat zła waluta, natomiast jeśli wpiszemy datę spoza zakresu dat w bazie,
dostaniemy komunikat zła data.

3.Limity
Limity zostały ustawione w settings.py. Dla użytkownika jest to 12 zapytań na minutę, 100 na godzinę, a dla anon 10 na minutę i 100 na godzinę.

