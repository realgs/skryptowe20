Lista 5 API

Do uruchomienia programu potrzebny jest Python (w wersji 3), oraz pobrany do niego framework Django.
Wchodząc w środowisko programistyczne PyCharm, po wpisaniu w terminalu komendy 'python manage.py runserver' uzyskujemy link aby przejść do API.

Postawowe działanie:
Po uruchomieniu programu pojawia się domyślnie wybrana data, wyświetlają się notowania dolara w tym dniu. 
Aby sprawdzić notowanie dolara z innego dnia np. 9 września 2014 należy wpisać /usd/2014-09-09 w ścieżce URL.
Jeśli użytkownik wybierze datę spoza posiadanego zakresu pojawi się o tym komunikat.
Każde notowanie ma dodatkową informację interpolated, która przyjmuje wartość true, gdy wartość była pobrana z dnia poprzedzającego notowanie. 

Jeśli użytkownik chce sprawdzić informację o łącznej sprzedaży danego dnia np. 1 stycznia 2015 należy wpisać /sales/2015-01-01. 
Wyświetlana jest ona w dwóch walutach.

API jest zabezpieczone przed zbyt częstymi zapytaniami - użytkownik ma ograniczenie 10 zapytań na minutę oraz dodatkowo 30 zapytań na godzinę. 
Anon - 10 zapytań na minutę.
