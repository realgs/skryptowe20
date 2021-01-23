#Szkodziński Kacper 244008 Języki Skryptowe - DVD RENTAL API

##Wstęp
Niniejsze API umożliwia użytkownikowi sprawdzenie podsumowania transakcji z 
wybranego okresu, podliczając zyski w dwóch walutach, oraz sprawdzenie użytych 
do liczenia zysków kursów USD z danych okresów. 
Komunikacja z serwisem polega na wysłaniu odpowiednio sparametryzowanego żądania
HTTP GET pod adres http://127.0.0.1:5000/.

Do korzystania z API wymagane jest połączenie z bazą danych dvdrental,
przechowywaną lokalnie na maszynie należącej do wypożyczalni pod adresem
postgres://postgres:bazman@localhost:5432/dvdrental.

##Instalacja zależności
Wszystkie zależności można znaleźć w specjalnie przygotowanym pliku 
requirements.txt.

Instalacje można uprościć do wywołania komendy *pip install -r requirements.txt*

##Instrukcja użytkowania

###Informacje ogólne
- Odpowiedź serwisu zwracana jest w formacie json.

- Dane archiwalne dotyczące kursów USD i podsumowań transakcji dostępne są w
przedziale czasu od **2017-08-30** do **2020-12-11**, kiedy to sklep zawiesił
działalność, wygryziony z rynku przez serwisy streamingowe.
Właściciel sklepu zaznacza sobie jednak możliwość edycji tych dat, w razie gdyby
działalność wypożyczalni została wznowiona.
 
###Opis funkcji API dotyczącej kursów
Funkcja pobierająca kursy USD w stosunku do PLN znajduje się pod adresem:
http://127.0.0.1:5000/api/v1/resources/exchangerates

Przyjmuje następujące atrybuty opcjonalne:
- startdate - określa początek zakresu wyszukiwania. Domyślnie ustawiony jest
na najwcześniejszą datę w bazie. Format DD/MM/RR.
- enddate - określa koniec zakresu wyszukiwania. Domyślnie ustawiony jest
 na najpóźniejszą datę w bazie. Format DD/MM/RR.

Przykłady:
- Pobranie wszystkich kursów w bazie:
 http://127.0.0.1:5000/api/v1/resources/exchangerates
- Pobranie wszystkich kursów od 9 września 2018 roku:
 http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=9/9/18
- Pobranie wszystkich kursów do 9 września 2018 roku:
 http://127.0.0.1:5000/api/v1/resources/exchangerates?enddate=9/9/18
- Pobranie wszystkich kursów między 3 grudnia 2017 roku a 9 grudnia 2017 roku:
 http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=3/12/17&enddate=9/12/17

###Opis funkcji API dotyczącej podsumowań transakcji
Funkcja pobierająca podsumowania transakcji z informacjami o ich ilości i łącznym
 przychodzie w dwóch walutach. Występuje w dwóch wersjach:
 - Zapytanie o transakcje z konkretnego dnia:
 http://127.0.0.1:5000/api/v1/resources/salessummary
 - Zapytanie o transakcje z przedziału dni:
 http://127.0.0.1:5000/api/v1/resources/salessummary/range

####Zapytanie o konkretny dzień
Wymaga podania atrybutu **date**, który wskazuje, o jaki dzień pytamy.
 Format DD/MM/RR. 
 
Przykład - 
Informacje o transakcjach z 12 grudnia 2018 roku:
http://127.0.0.1:5000/api/v1/resources/salessummary?date=12/12/18

####Zapytanie o przedział dni
Przyjmuje następujące atrybuty opcjonalne:
- **startdate** - określa początek zakresu wyszukiwania. Domyślnie ustawiony jest
na najwcześniejszą datę w bazie. Format DD/MM/RR.
- **enddate** - określa koniec zakresu wyszukiwania. Domyślnie ustawiony jest
 na najpóźniejszą datę w bazie. Format DD/MM/RR.

Przykłady:
- Pobranie podsumowania wszystkich transakcji w bazie:
 http://127.0.0.1:5000/api/v1/resources/salessummary/range
- Pobranie podsumowania wszystkich transakcji w bazie od 9 września 2018 roku:
 http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=9/9/18
- Pobranie podsumowania wszystkich transakcji w bazie do 9 września 2018 roku:
 http://127.0.0.1:5000/api/v1/resources/salessummary/range?enddate=9/9/18
- Pobranie podsumowania wszystkich transakcji w bazie między 3 grudnia 2017
 roku a 9 grudnia 2017 roku:
 http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=3/12/17&enddate=9/12/17
 
###Ograniczenia
- Pojedyńczy użytkownik nie może zadać więcej niż 60 zapytań na minutę.
- Użytkownik który przekroczy limit musi odczekać aż limity zostaną odświeżone.
 
###Komunikaty błędów
 - W przypadku zadania nieprawidłowo sformułowanych zapytań serwis zwraca komunikat 400 Bad
 Request wraz z wypisanym powodem i podpowiedzią użytkowania.
 - W przypadku przekroczenia limitu zapytań na minutę serwis zwraca komunikat
  429 Too Many Requests. 