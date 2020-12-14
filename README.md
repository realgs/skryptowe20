# API - lista 5
## Michał Chrobot 246665

W programie użyłem następujących technologii:
* Python 3.8.3
* Flask
* SQLite3

### Instalacja i uruchomienie

```bash
pip install flask
pip install Flask-Limiter
```

Do uruchomienia aplikacji potrzebna będzie też baza danych sqlite

Baza danych, z której korzystałem do wykonania tego zadania można znaleźć [tutaj](https://github.com/jpwhite3/northwind-SQLite3).

Należy z powyższej strony pobrać plik "Northwind_large.sqlite", następnie stworzyć w projekcie folder o nazwie "database_files" i dodać tam rozpakowaną bazę o zmienionej nazwie na "Northwind.sqlite" 

Aby aplikacja zaczęła działać należy uruchomić skrypt api.py


### Adresacja

Notowania z konkretnego dnia lub zakresu dat wraz z informacją 'interpolated':
```python
GET http://127.0.0.1:5000/USD/<ratingDate>
GET http://127.0.0.1:5000/USD/<dateFrom>/<dateTo> 
```
Suma sprzedaży wraz z przeliczeniem po kursie z danego dnia, lub zakresu dat:
```python
GET http://127.0.0.1:5000/sales/<salesDate>
GET http://127.0.0.1:5000/sales/<dateFrom>/<dataTo>
```
Data powinna być podana w formacie 2020-07-12, w przeciwnym wypadku zostanie zwrócony kod błędu 400.
Również jeżeli data początkowa jest większa od daty końcowej lub data końcowa jest >= od aktualniej daty to zwrócony zostanie kod błędu 416

### Limity

Limity nałożone są na adres sieciowy użytkownika i mają następujące ograniczenia:
* Zapytania o notowania z konkretnego dnia: **10 na minutę**
* Zapytania o notowania z zakresu dat: **60 na minutę**
* Zapytania o sprzedaż z konkretnego dnia: **10 na minutę**
* Zapytania o sprzedaż z zakresu dat: **60 na minutę**

Nałożone jest również limit na sumę wszystkich zapytań API i wynosi on **200 na minutę**

Zaimplementowane są również domyślne limity.

Odpowiedzią na przekroczony limit zapytań jest kod błędu **429**.

## Struktura projektu

* **api.py** - główny program FLASK'a odpowiedzialny za API
* **database.py** - plik zawierający funkcje pozwalające na pobranie danych z bazy
