# Instrukcja uruchomienia
Przed uruchomieniem programu należy posiadać na komputerze program python3 oraz mieć do niego paczki:
flask, sqllite3 oraz requests 

Aby uruchomić program wystarczy zaciągnąć pliki na dysk oraz posiadać bazę danych wykorzystywaną
w zadaniu.

Uruchamiamy api wykonując skrypt main.py. Jeśli robimy to po raz drugi należałoby zakomentować linie
odpowiadające za generację i wypełnienie bazy danych, a więc pierwsze dwie. 

Należy udać się na stronę http://127.0.0.1:500/ aby zacząć korzystać z API.
 
 
# Zaimplementowane endpointy:
* <b>/api/rates/fordate?date=value<b>
    * zapytanie GET zwraca nam kurs waluty USD w przeliczeniu na PLN na dany dzień podany w parametrze value

* <b>/api/rates/fordatespan?from=value1&to=value2</b>
  * zapytanie GET zwraca kursy waluty US w przeliczeniu na PLN dla przedziału dni podanych w parametrach 
    od value1 do value2


# Zwracane kody:
 - 200 -> success
 - 401 -> błąd po stronie klienta, np niepoprawne dane lub ich brak
 - 501 -> błąd po stronie serwera, np. nie znaleziono danych w bazie danych

