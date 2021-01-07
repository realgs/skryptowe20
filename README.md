# MyWebAPI
## Co to?
MyWebAPI to API pozwalające na dostęp do kursów dolara i złotówek oraz podsumowań sprzedaży z przykładowej bazy transakcji. Kursy pochodzą z API NBP http://api.nbp.pl/, a baza danych z https://www.sqlitetutorial.net/sqlite-sample-database/
## Czego potrzebujemy żeby to uruchomić?
- Python
- pip (https://pip.pypa.io/en/stable/installing/)
- Flask (pip install Flask)
- Flask-Limiter (pip install Flask-Limiter)
## Jak to uruchomić?
Przejdź do folderu lab5 w projekcie i uruchom w nim konsolę i wpisz "python app.py". 
Jeśli wszystko poszło dobrze, powinieneś zobaczyć w konsoli komunikat "Running on http://127.0.0.1:5000/".
Aby przetestować działanie, przejdź na stronę (http://127.0.0.1:5000/api/exchangerate/usd/2010-01-01/).
Powinna się tam wyświetlić odpowiedź w postaci JSONa.
## Jakie zapytania mogę tworzyć?
### 1. /api/exchangerate/{waluta}/{data}
Zwraca kurs waluty z danej daty w formacje JSON.

**Pola w zapytaniu:**  
- waluta - PLN lub USD. Wielkość liter nie ma znaczenia. Jeśli wybierzemy PLN, wynikiem będzie cena 1 złotówki w dolarach.  
Jeśli wybierzemy USD, wynikiem będzie cena 1 dolara w złotówkach.  
- data - w formacie rok-miesiąc-dzień (np. 2010-01-15, 2009-10-02, 2009-06-07). Data musi być pomiędzy 1 stycznia 2009 a 31 grudnia 2010 (włącznie).  

**Pola w odpowiedzi:**  
- code - trzyliterowy kod waluty  
- day - dzień którego dotyczy żądanie  
- interpolated - przyjmuje wartość false jeśli kurs został tego dnia opublikowany przez NBP, a wartośc true jeśli kurs został wyznaczony na podstawie kursu z poprzedniego dnia.  
- rate - kurs wymiany  

**Komunikaty o błedach:**
- 400:BadRequest. UnknownCurrency - podano nieprawidłowy kod waluty. Kodem waluty może być jedynie USD albo PLN (wielkośc liter nie ma znaczenia).
- 400:BadRequest. Date out of range - podano nieprawidłową datę. Data musi być pomiędzy 1 stycznia 2009 a 31 grudnia 2010 (włącznie).

### 2. /api/exchangerate/{waluta}/{data_od}/{data_do}
Zwraca kurs waluty w dniach pomiędzy data_od a data_do (włącznie) w formacje JSON.
**Pola w zapytaniu:**
- waluta - PLN lub USD. Wielkość liter nie ma znaczenia. Jeśli wybierzemy PLN, wynikiem będzie cena 1 złotówki w dolarach.  
Jeśli wybierzemy USD, wynikiem będzie cena 1 dolara w złotówkach.  
- data_od, data_do - w formacie rok-miesiąc-dzień (np. 2010-01-15, 2009-10-02, 2009-06-07)
data_od musi być równa lub wcześniejsza niż data_do.

**Pola w odpowiedzi:**
- code - trzyliterowy kod waluty
W kolejnych rekordach:
- day - dzień którego dotyczy rekord
- interpolated - przyjmuje wartość false jeśli kurs został tego dnia opublikowany przez NBP, a wartośc true jeśli kurs został wyznaczony na podstawie kursu z poprzedniego dnia.
- rate - kurs wymiany

**Komunikaty o błędach:**
- 400: BadRequest. UnknownCurrency - podano nieprawidłowy kod waluty. Kodem waluty może być jedynie USD albo PLN (wielkośc liter nie ma znaczenia).
- 400: BadRequest. Date out of range - podano nieprawidłową datę. data_od musi być równa lub wcześniejsza niż data_do.

**Uwagi:**
Jeśli data_od jest wcześniejsza niż 1 stycznia 2009, program przyjmie że data_od to 1 stycznia 2009. Jesli data_do jest późniejsza niż 31 grudnia 2010, program przyjmie że data_do to 31 grudnia 2010.
Sprawia to że zapytanie o kursy pomiędzy 10 kwietnia 2008 a 6 stycznia 2009 zwróci kursy pomiędzy 1 stycznia 2009 a 6 stycznia 2009.


### 3. /api/sales/{data}
Zwraca podsumowanie sprzedaży z danej daty w formacje JSON.

**Pola w zapytaniu:**
- data - w formacie rok-miesiąc-dzień (np. 2010-01-15, 2009-10-02, 2009-06-07). Data musi być pomiędzy 1 stycznia 2009 a 31 grudnia 2010.

**Pola w odpowiedzi:**
- day - dzień którego dotyczy żądanie
- number of sales - łączna liczba transakcji do których doszło danego dnia
- sales_pln - suma kwót transakcji w złotówkach przeliczonych po kursie NBP z danego dnia
- sales_usd - suma kwót transakcji w dolarach

**Komunikaty o błędach:**
- 400: BadRequest. Date out of range - podano nieprawidłową datę. data musi być pomiędzy 1 stycznia 2009 a 31 grudnia 2010.

**Uwagi:**
Jeśli zapytanie zwróci 0 jako liczbę transakcji i sumy kwót oznacza to, że danego dnia nie została zawarta żadna transakcja.

### 4. /api/sales/{data_od}/{data_do}
Zwraca podsumowanie sprzedaży w dniach pomiędzy data_od a data_do w formacje JSON.

**Pola w zapytaniu:**
- data_od, data_do - w formacie rok-miesiąc-dzień (np. 2010-01-15, 2009-10-02, 2009-06-07). data_od musi być równa lub wcześniejsza niż data_do.

**Pola w odpowiedzi:**
W kolejnych rzędach:
- day - dzień którego dotyczy rekord
- number of sales - łączna liczba transakcji do których doszło danego dnia
- sales_pln - suma kwót transakcji w złotówkach przeliczonych po kursie NBP z danego dnia
- sales_usd - suma kwót transakcji w dolarach

**Komunikaty o błędach:**
- 400: BadRequest. Date out of range - podano nieprawidłową datę. data_od musi być równa lub wcześniejsza niż data_do.

**Uwagi:**
Jeśli zapytanie dla któregoś dnia zwróci 0 jako liczbę transakcji i sumy kwót oznacza to, że danego dnia nie została zawarta żadna transakcja.
Jeśli data_od jest wcześniejsza niż 1 stycznia 2009, program przyjmie że data_od to 1 stycznia 2009. Jesli data_do jest późniejsza niż 31 grudnia 2010, program przyjmie że data_do to 31 grudnia 2010.
Sprawia to że zapytanie o podsumowanie sprzedaży w dniach od 10 listopada 2010 a 12 stycznia 2011 zwróci podsumowanie z dni od 10 listopada 2010 do 31 grudnia 2010.


## Przykładowe zapytania:
- **/api/exchangerate/USD/2009-06-05** - kurs wymiany złotówek na dolary z 5 czerwca 2009.
- **/api/exchangerate/PLN/2010-10-21** - kurs wymiany dolara na złotówki z 21 października 2010.
- **/api/exchangerate/USD/2009-02-04/2009-05-24** - kursy wymiany złotówek na dolary pomiędzy 2 lutego 2009 a 24 maja 2009 (włącznie).
- **/api/exchangerate/PLN/2009-12-13/2010-12-13** - kursy wymiany dolarów na złotówki pomiędzy 13 grudnia 2009 a 13 grudnia 2010 (włącznie).
- **/api/sales/2009-12-24** - podsumowanie sprzedaży z dnia 24 grudnia 2010 roku.
- **/api/sales/2009-01-02** - podsumowanie sprzedaży z 2 stycznia 2009 roku
- **/api/sales/2010-01-01/2010-01-31** - podsumowania sprzedaży pomiędzy 1 stycznia 2010 a 31 stycznia 2010 (włącznie).
- **/api/sales/2009-10-10/2010-01-10** - podsumowania sprzedaży pomiędzy 10 października 2009 a 10 stycznia 2010 (włącznie)

## Jakie pliki znajdują się w projekcie?
- **app.py** - główny plik programu, to on odpowiada za wystawianie danych użytkownikowi i pobieranie ich z bazy
- **create_exchange_rates_in_table.py** - dodaje do bazy danych 'chinook.db' do tabeli 'exchange_rates' kursy walut pomiędzy 1 stycznia 2009 a 31 stycznia 2010 pobierane z api NBP
- **calculate_total_sales.py** - dodaje do bazy danych 'chinook.db' do tabeli 'total_sales' podsumowanie sprzedaży z tej bazy danych.
- **chinook.db** - baza danych wykorzystywana w ćwiczeniu. Pochodzi z https://www.sqlitetutorial.net/sqlite-sample-database/ i została uzupełniona przez wykonanie skryptów 'create_exchange_rates_in_table.py' oraz 'calculate_total_sales.py' 

## Coś jeszcze?
Korzytanie z API jest objęte limitem czasowym. Kazdy użytkownik może wykonać maksymalnie 10 zapytań na minutę. Kolejne zapytania będą odrzucane, a użytkownik otrzyma komunikat 429: TooManyRequests. Limity zapytań można zmienić w pliku app.py.
