# API - lista 5
## Kacper Gąsior 246645

W programie użyte zostały następujące technologie:
1. **Python 3.7.7**
2. **Flask**
3. **SQLite3**

### Uruchomienie programu

Należy zainstalować następujące pakiety:
```
pip install Flask
pip install Flask-Limiter
pip install Flask-Cashing
pip install requests
```

Kursy walut pobierane są z api **NBP** http://api.nbp.pl/
Kursy są dostępne od dnia **2002-01-02**

Do uruchomienia aplikacji potrzebna będzie też baza danych sqlite **orders.db**<br/>
Warto mieć na uwadze, że baza ta zawiera dane o sprzedaży z zakresu dat od **2009-01-01** do **2012-12-30**

Aby aplikacja zaczęła działać należy uruchomić skrypt **myCurrencyApi.py**

### Limity

Limity nałożone na adres sieciowy użytkownika mają następujące ograniczenia:
* Zapytania o notowania z konkretnego dnia: **300 zapytań na minutę**
* Zapytania o notowania z zakresu dat: **100 zapytań na minutę**
* Zapytania o sprzedaż z konkretnego dnia: **300 zapytań na minutę**
* Zapytania o sprzedaż z zakresu dat: **100 zapytań na minutę**

Nałożony jest również limit na sumę wszystkich zapytań API i wynosi on **200 zapytań na minutę**

Odpowiedzią na przekroczony limit zapytań jest kod błędu **429**

### Cache

Mechanizm cache'u zaimplementowany w zadaniu sprawdza czy zapytanie zostało wykonane wcześniej.</br>
**Jeśli tak** - zwraca zapamiętaną wartość,</br>
**jeśli nie** - zapamiętuje odpowiedź na zapytanie.

Cache odświeża się co **1 godzinę**, aby zapobiec przepełnieniu pamięci

### Adresowanie

Notowanie wybranej waluty z konkretnego dnia razem z informacją czy jest interpolowana:
```
GET http://127.0.0.1:5000/api/v1/resources/rates/<currency>/<search_date>/
```
Notowanie waluty USD z zakresu dat razem z informacją czy jest interpolowana:
```
GET http://127.0.0.1:5000/api/v1/resources/rates/<currency>/<start>/<end>/

```
Suma sprzedaży z konkretnego dnia w walutach PLN i USD:
```
GET http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/<search_date>/
```
Suma sprzedaży z zakresu dat w walutach PLN i USD:
```
GET http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/<start>/<end>/
```
Data powinna być podana w formacie ISO 8601 np. 2020-07-12. W przeciwnym wypadku zostanie zwrócony kod błędu **400**.<br/>
Jeżeli data początkowa jest większa od daty końcowej lub data końcowa jest >= od aktualniej daty to zwrócony zostanie kod błędu **416**

### Struktura projektu

1. **myCurrencyApi.py** - główny program odpowiedzialny za funkcjonowanie API i zarządzanie danymi zwracanymi przez aplikację
2. **ordersDbMethods.py** - plik zawierający funkcje pozwalające na pobranie danych o sprzedaży z bazy
3. **currencyMethods.py** - plik zawierający funkcje pozwalające na pobranie danych z API NBP
4. **orders.db** - plik bazy danych zawierający sprzedaż firmy Superstore
