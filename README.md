# API - lista 5
## Michał Chrobot 246665

W programie użyte zostały następujące technologie:
1. **Python 3.8.3**
2. **Flask**
3. **SQLite3**

### Uruchomienie programu

Należy zainstalować następujące pakiety:
```
pip install flask
pip install Flask-Limiter
```

Do uruchomienia aplikacji potrzebna będzie też baza danych sqlite,<br/>
baza danych z której korzystałem do wykonania tego zadania można znaleźć [pod tym linkiem](https://github.com/jpwhite3/northwind-SQLite3)<br/>

Należy z powyższej strony pobrać plik "Northwind_large.sqlite", następnie stworzyć w projekcie folder o nazwie "database_files" i dodać tam rozpakowaną bazę o zmienionej nazwie na "Northwind.sqlite"<br/>
Warto mieć na uwadze, że baza ta zawiera dane o sprzedaży z zakresu dat od **2012-07-04** do **2016-02-19**

Aby aplikacja zaczęła działać należy uruchomić skrypt api.py

### Limity

Limity nałożone na adres sieciowy użytkownika mają następujące ograniczenia:
* Zapytania o notowania z konkretnego dnia: **10 na minutę**
* Zapytania o notowania z zakresu dat: **60 na minutę**
* Zapytania o sprzedaż z konkretnego dnia: **10 na minutę**
* Zapytania o sprzedaż z zakresu dat: **60 na minutę**

Nałożone jest również limit na sumę wszystkich zapytań API i wynosi on **200 na minutę**

Odpowiedzią na przekroczony limit zapytań jest kod błędu **429**

### Adresowanie

Notowanie waluty USD z konkretnego dnia razemz informacją 'interpolated':
```
GET http://127.0.0.1:5000/USD/<ratingDate>
```
Notowanie waluty USD z zakresu dat razem z informacją 'interpolated':
```
GET http://127.0.0.1:5000/USD/<dateFrom>/<dateTo> 
```
Suma sprzedaży z konkretnego dnia w walutach PLN i USD (sumy te są podane w polach "sumPLN" i "sumUSD" zwracanego pliku JSON):
```
GET http://127.0.0.1:5000/sales/<salesDate>
```
Suma sprzedaży z zakresu dat w walutach PLN i USD (sumy te są podane w polach "sumPLN" i "sumUSD" zwracanego pliku JSON, zwracane są także wyniki z każdego dnia):
```
GET http://127.0.0.1:5000/sales/<dateFrom>/<dataTo>
```
Data powinna być podana w formacie 2020-07-12, w przeciwnym wypadku zostanie zwrócony kod błędu **400**.<br/>
Również jeżeli data początkowa jest większa od daty końcowej lub data końcowa jest >= od aktualniej daty to zwrócony zostanie kod błędu **416**

### Struktura projektu

1. **api.py** - główny program odpowiedzialny za funkcjonowanie API, zawiera funkcje pozwalające na pobieranie danych z API NBP i zarządzanie danymi zwracanymi przez aplikację
2. **database.py** - plik zawierający funkcje pozwalające na pobranie danych o sprzedaży z bazy
