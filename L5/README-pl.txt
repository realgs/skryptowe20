# Moje API

## Wprowadzenie
Moje API służy do pozyskania informacji na temat notowań USD/PLN w latach 2013-2016
oraz wartości łącznej sprzedaży produktów w tych latach

## Technologie
 - Python 3.7.4
    W celu zainstalowania Pythona odwiedź stronę https://www.python.org/downloads/ 
    Wersję Pythona można sprawdzić w wierszu poleceń za pomocą komendy: python --version
 - pip
    Jeżeli pobierałeś Pythona z zaproponowanej strony, powinieneś mieć go już zainstalowanego.
    Jeżeli nie masz zainstalowanego pip, skorzystaj ze strony https://pypi.org/project/pip/ lub https://pip.pypa.io/en/stable/installing/
    Wersję pip można sprawdzić w wierszu poleceń za pomocą komendy: pip --version
 - Flask
 - Flask-Limiter
 - sqlite3
 - datetime
 - requests
    W celu zainstalowania brakujących bibliotek w wierszu poleceń wpisz: pip install {nazwa biblioteki}

## Uruchomienie
W celu rozpoczęcia działania aplikacji uruchom plik api.py.
Możesz to zrobić np. w wierszu poleceń za pomocą komendy: python {ścieżka do pliku api.py}
W celu przetestowania działania aplikacji przejdź na stronę http://127.0.0.1:5000/
Na stronie powinna pojawić się krótka instrukcja obsługi api.

## Opis funkcji API
Odpowiedź serwisu jest zwracana w formacie JSON.
Kod odpowiedzi w przypadku powodzenia to 200.

### Parametry zapytań
 - {date}, {start_date}, {end_date} - data w formacie RRRR-MM-DD (standard ISO 8601)

### Dostępne zapytania
 - Zapytanie o kurs dolara w dniu {date}:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/{date}/
 - Zapytanie o kursy dolara od {start_date} do {end_date}:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/{start_date}/{end_date}/
 - Zapytanie o sumę sprzedaży w dniu {date}:
    http://127.0.0.1:5000/api/v1/salesdata/{date}/
 - Zapytanie o sumy sprzedaży od {start_date} do {end_date}:
    http://127.0.0.1:5000/api/v1/salesdata/{start_date}/{end_date}/

### Parametry odpowiedzi
 - date - data notowania/sprzedaży
 - interpolated - typ notowania (true - przybliżone na podstawie poprzedniego znanego kursu, false - zgodne z kursem NBP)
 - PLN - łączna wartość sprzedaży w złotówkach
 - rate - kurs wymiany
 - USD - łączna wartość sprzedaży w dolarach amerykańskich

### Komunikaty błędów
 - W przypadku zapytania o nieznanej strukturze ścieżki zwracany jest kod odpowiedzi 404 i komunikat:
    The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
 - W przypadku przekroczenia dostępnej liczby zapytań na jednostkę czasu zwracany jest kod odpowiedzi 429 i komunikat:
    10 per 1 minute
 - W przypadku zapytania o datę spoza zakresu zwracany jest komunikat:
    404 NotFound - Brak danych / No data available
 - W przypadku zapytania zawierającego nieprawidłowo sformułowaną datę zawracany jest komunikat:
    400 Bad Request - Niewlasciwy format daty / Invalid date format
 - W przypadku zapytania zawierającego nieprawidłowy zakres dat zwracany jest komunikat:
    400 BadRequest - Bledny zakres dat / Invalid date range

### Limity czasowe
Dla danego zapytania na użytkownika (adres IP) nałożony jest limit zapytań na jednostkę czasu: 10/min.

### Inne ograniczenia
W celu usprawnienia działania programu komunikacja z bazą danych jest ograniczona.
Otrzymane dane mogą być nieaktualne - czas odświeżenia danych wynosi nie więcej niż godzinę.

## Przykłady użycia
 - Zapytanie o kurs dolara w dniu 2015-12-12:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/2015-12-12/
 - Zapytanie o kursy dolara od 2014-01-01 do 2014-12-31:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/2014-01-01/2014-12-31/
 - Zapytanie o sumę sprzedaży w dniu 2016-03-20:
    http://127.0.0.1:5000/api/v1/salesdata/2016-03-20/
 - Zapytanie o sumy sprzedaży od 2013-01-01 do 2013-01-31:
    http://127.0.0.1:5000/api/v1/salesdata/2013-01-01/2013-01-31/

## Struktura
Projekt składa się z następujących plików:
 - api.py - plik z kodem odpowiedzialnym za komunikację z użytkownikiem,
 - sales_data_base.py - plik z kodem odpowiedzialnym za komunikację z bazą danych,
 - sales_data.db - plik zawierąjcy bazę danych.

## Możliwe modyfikacje

### Modyfikacja limitu zapytań na jednostkę czasu
W celu modyfikacji limitu zapytań należy w pliku api.py, w linijce 26, zmienić tekst "10 per minute" na docelowy.
Możliwe kombinacje: [count] [per|/] [n (optional)] [second|minute|hour|day|month|year]
Przykłady: "1 per second", "5 per 10 second", "100 per day"

### Modyfikacja maksymalnego czasu przechowywania danych w pamięci podręcznej serwera
W ceu modyfiacji maksymalnego czasu należy zmienić w pliku api.py, w linijce 10, fragment (hours=1).
Przykłady: (minutes=1), (seconds=30), (days=7), (hours=2, minutes=30) 
