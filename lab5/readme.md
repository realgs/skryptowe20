# Języki skryptowe - lista 5
## Mateusz Nasiadek 246669

### Jak uruchomić program

Aby uruchomić program należy wykonać poniższe komendy:
```
pip install Flask
pip install Flask-Limiter
pip install Flask-Cashing
pip install requests
```

Kursy dolara pobrane zostały z http://api.nbp.pl/ <br/>

Do uruchomienia aplikacji potrzebna będzie też baza danych orders.db<br/>
Warto mieć na uwadze, że baza ta zawiera dane o sprzedaży z zakresu dat od **2018-07-04** do **2020-05-06**
W związku z tym, kursy dolara też są dostępne w tym zakresie dat.

Aby uruchomić aplikację, należy uruchomić skrypt **api.py**

### Ścieżki URL 

Suma sprzedaży z danego dnia wyrażona w PLN i USD:
```
GET http://127.0.0.1:5000/api/sales/<sales_date>/
```
Suma sprzedaży z zakresu dat wyrażona w PLN i USD:
```
GET http://127.0.0.1:5000/api/sales/<start_date>/<end_date>/
```
Notowanie dolara z wybranej daty. Zapytanie zwraca też informację o interpolacji:
```
GET http://127.0.0.1:5000/api/rates/<rate_date>/
```
Notowanie dolara z zakresu dat. Zapytanie zwraca też informację o interpolacji:
```
GET http://127.0.0.1:5000/api/rates/<start_date>/<end_date>/
```

Data musi być podana w formacie ISO 8601 np. 2020-05-06. W przeciwnym wypadku zostanie zwrócony kod błędu 400.<br/>
Jeżeli data początkowa jest poźniejsza od daty końcowej lub daty wykraczają poza zakres to zwrócony zostanie kod błędu 416.

### Limity

Na każdy rodzaj zapytania nałożony jest limit zapytań z jednego adresu sieciowego, wynoszący **50 zapytań na minutę**.

Nałożony jest również limit na sumę wszystkich zapytań wynoszący **400 zapytań na minutę**

Odpowiedzią na przekroczony limit zapytań jest kod błędu **429**

### Cache

Mechanizm cache'u sprawdza czy zapytanie zostało wykonane wcześniej.<br/>
Jeśli tak - zwraca zapamiętaną wartość. Jeśli nie - zapamiętuje odpowiedź.

Cache odświeża się co **24 godziny**.

### Pliki

1. **api.py** - główny program odpowiedzialny za funkcjonowanie API
2. **db_getters.py** - plik, który zawiera funkcje pozwalające na pobranie danych z bazy
3. **database.py** - plik uruchomiony raz, aby poprawnie stworzyć i wypełnić potrzebne tabele w bazie danych
4. **nbp_requests.py** - plik pomocniczy przy tworzeniu tabel w bazie danych
5. **database.db** - plik bazy danych 