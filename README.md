Wymagane programy:
- pytohn3
- docker
- psql

Wymagane paczki python3:
- flask
- flask_limiter
- psycopg2

Sposób uruchomienia:
1.) Uruchamiamy skrypt instalujący bazę danych postgres - ./configuredb.sh
2.) Przechodzimy do katalogu src/main/
3.) Uruchamiamy serwer komendą: python3 app.py


Endpointy:

1.) /api/rates/<currency_code>'
Parametry:
startDate-
endDate-


2.) /api/sales/<currency_code>
Parametry:
date-
endDate-


Liczba zapytań jest organiczona do 10 na minutę. 
Limit nakładany jest na każdy adres ip osobno. 
