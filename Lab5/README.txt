1. Uruchomienie 
Żeby uruchomić program należy posiadać na komputerze Pythona w wersji 3 oraz dodatki do niego, takie jak:
-django
-sqlite3
-request
Należy również posiadać odpowiednią bazę danych, z której korzysta program.

Projekt był tworzony w pyCharm (używając Anacondy), więc jest on ułożony w katalogi. 
Najpierw utoworzony został zwykły nowy projekt w pychar, potem dzięki komendzie django-admin stratproject {nazwa} wpisanej w terminal 
projekt django, a następnie poprzez komendę python manage.py startapp {nazwainna} utorzył się katalog właściwej aplikacji.
Tutaj dodane są tylko 4 pliki, z tych które tworzą się automatycznie po stworzeniu nowego projektu, ponieważ tylko one zostały zmienione. 
Program uruchamia się korzystając z terminala i wpisując komendę: python manage.py runserver. 
Otrzymujemy wtedy link do naszego API.

2.Pobieranie danych
Z API można pobrać dwie rzeczy - notowanie usd lub sprzedaż z danego dnia. Możemy po url API wpisać:
-/usd/data - pobierzemy notowanie usd z wybranego dnia (format yyyy-mm-dd) z bazy danych sprzedaży, np.usd/2015-01-01.
-/sales/data - pobierzemy łączą sumę sprzedaży z podanej daty (format yyyy-mm-dd) z bazy danych sprzedaży, np.sales/2015-01-01.
Gdy data będzie spoza zakresu zapisanego w bazie, pojawi się komunikat data spoza zakresu, natomiast jeśli data będzie z zakresu i tego dnia nie było sprzedaży
pojawi się komunikat o barku sprzedaży. W innych przypadkach zobaczymy odpowiednie informacje.
Kiedy poprosimy o notowanie, dostaniemy jego numer, datę, wartość oraz odpowiedź, czy notowanie jest z tego dnia, czy z jednego z poprzednich w interpolated.
Kiedy poprosimy o sprzedaż dostaniemy numer, datę, sprzedaż w usd i pln.

3.Limity
Limity zostały ustawione w settings.py. Dla użytkownika jest to 12 zapytań na minutę, 100 na godzinę, a dla anon 10 na minutę i 100 na godzinę.

