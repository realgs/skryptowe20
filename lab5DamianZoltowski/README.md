# Instrukcja uruchomienia
Przed uruchomieniem programu należy posiadać na komputerze program python3 oraz mieć do niego paczki:
flask, flask_limiter, sqllite3 oraz requests 

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

* <b></api/sales/forday?date=value</b>
    * zapytanie GET zwraca łączną sumę sprzedaży w walucie PLN oraz USD dla dnia podanego jako value

# Zwracane kody:
 - 200 -> success
 - 401 -> błąd po stronie klienta, np niepoprawne dane lub ich brak
 - 501 -> błąd po stronie serwera, np. nie znaleziono danych w bazie danych

# Limity
* Limity są przypisane po IP użytkownika, który wysyła zapytanie.
* Podstawowy limit requestów jakie możemy wykonać to 300 na dzień.
* Zapytanie o wartość dolara w PLN dla konkretnego dnia możemy wykonać nie częściej niż 15 razy na minutę
 i nie częściej niż 100 razy na godzinę.
* Zapytanie o wartości dolara w PLN dla przedziału dat możemy wykonać nie częściej niż 5 razy na minutę
 i nie częściej niż 70 razy na godzinę.
* Zapytanie o wartości sprzedaży w PLN i USD w danym dniu możemy wykonać nie częściej niż 10 razy na minutę
i nie częściej niż 90 razy na godzinę.