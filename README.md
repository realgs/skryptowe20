Frontend-app:

Wymagane programy:
- docker

Sposób uruchomienia:
 - 1.) Uruchamiamy aplikacje komenda: 'docker-compose up' z poziomu katalogu lab6 
 ( Trochę to niestety trwa. Jeśli wystąpi jakiś błąd związany z exchange-api, proszę powtórzyć)
 - 2.) Uruchamiamy przeglądarkę ( najlepiej google chrome )
 - 3.) Przechodzimy pod adres: localhost:5000

API :

Wymagane programy:
- docker

Sposób uruchomienia:
 - 1.) Uruchamiamy aplikacje komenda: docker-compose up

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


Liczba zapytań jest organiczona do 10 na sekundę. 
Limit nakładany jest na każdy adres ip osobno. 
