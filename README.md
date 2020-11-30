Wymagane programy:
- pytohn3
- docker
- psql

Wymagane paczki python3:
- flask
- flask_limiter
- psycopg2

Sposób uruchomienia:
 - 1.) Uruchamiamy skrypt instalujący bazę danych postgres - ./configuredb.sh
 - 2.) Przechodzimy do katalogu src/main/
 - 3.) Uruchamiamy serwer komendą: python3 app.py

Endpointy:

1.) /api/rates/<currency_code>
- Parametry zapytania:
    - <currency_code> - kod waluty dla oczkiwanych rat ( Wspierane waluty: EUR, USD, CHF, GBP, TRY, AUD, RUB )
- Parametry ścieżki:
    - startDate - data początowa rat (np. 2020-11-22)
    - endDate - data końcowa rat (np. 2020-11-28)


2.) /api/sales/<currency_code>
- Parametry zapytania:
    - <currency_code> - kod waluty dla podsumowania sprzedaży ( Wspierane waluty: EUR, USD, CHF, GBP, TRY, AUD, RUB )
- Parametry ścieżki:
    - date - dzień, dla którego podsumowujemy sprzedaż (np. 2020-11-22)


Przykładowe zapytania:

- localhost:8080/api/rates/USD?startDate=2020-11-22&endDate=2020-11-28
- localhost:8080/api/sales/USD?date=2020-11-22


Liczba zapytań jest organiczona do 10 na minutę. 
Limit nakładany jest na każdy adres ip osobno. 
