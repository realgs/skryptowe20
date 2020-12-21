# Wystawianie własnego API - Lista 5 #
## Robert Hejda - 246694 ##
## Wstęp ##
Do utworzenia api wykorzystano następujące technologie:
* Python v. 3.7.6
* MongoDB v. 4.4.2
* Dodatkowe biblioteki, pakiety do Python, zawarte w pliku requirements.txt

API zostało oparte o framework FastAPI.

Jako zbiór danych wykorzystano zbiór Sample Supply Store Dataset pobrany z https://github.com/huynhsamha/quick-mongo-atlas-datasets 

## Uruchomienie ##
* Przed uruchomieniem API należy zainstalować konieczne pakiety, co można zrobić poniższą komendą:
        
        pip install -r requirements.txt
* Należy pobrać i zaimportować bazę danych, opis tych czynności znajduje się na https://github.com/huynhsamha/quick-mongo-atlas-datasets 
* Należy przygotować dodatkowe tabele do API poprzez uruchomienie skryptu database_preparation.py
* Aby uruchomić API, należy uruchomić skrypt api.py

Z poziomu Windows 10 skrypty można uruchomić poprzez wywołanie:

        python api.py
## Endpointy ## 
Domyślnie API uruchamia się na localhost:8000
* **/api/exchangerates/{date}** - Wartość dolara względem złotego opublikowana w dniu date
* **/api/exchangerates/{start_date}/{end_date}** - Tabela wartości dolara względem złotego w przedziale czasowym start_date, end_date
* **/api/transactions/date** - Łączna wartość transakcji w dniu date

## Przykłady ##
* **/api/exchangerates/2014-01-01** - zwróci wartość kursu wymiany dolara na złotówkę w dniu 2014-01-01
* **/api/exchangerates/2014-01-01/2015-01-01** - zwróci wartość kursów wymiany dolara na złotówkę w przedziale czasowym od 01.01.2014 do 01.01.2015 
* **/api/transactions/2014-01-03/** - zwróci informację o wartości transakcji w dniu 03.01.2014
* **/api/transactions/2014-01-01/** - zwróci informację o braku danych dla wskazanej daty

## Pliki ##
Projekt składa się z kilku plików
* api.py - plik, poprzez który uruchamiamy API
* database_operation.py - operacje wstępne na źródłowej bazie danych
* crud.py - operacje CRUDowe
* schemas.py - modele Pydantic do walidacji danych

## Inne ##
* Aplikacja przy łączeniu z bazą danych używa prostego mechanizmu cachowania
* Jedno IP może wykonać do 5 żądań na minutę, które zwracają listy; do 50 żądań na minutę zwracających pojedynczy wynik i do 300 żądań na dzień.
