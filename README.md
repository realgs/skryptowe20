## Co jest w repo i jak to uruchomić?
Repozytorium składa się z 2 folderów: "api" i "interface". W "api" znajduje się API z poprzedniego laboratorium napisane we Flasku. 
W "interface" znajduje się interfejs graficzny do obsługi API napisany w Django.

Aby uruchomić interfejs potrzebujemy:
- Pythona
- pip (https://pip.pypa.io/en/stable/installing/)
- Django (pip install django)

Gdy mamy już zainstalowane te 3 rzeczy, w folderze "interface" wykonujemy komendę "python manage.py runserver". 
Jeśli wszystko poszło dobrze, powinniśmy otrzymać komunikat "Starting development server at http://127.0.0.1:8000/".
Przejdź na tę stronę w przeglądarce, aby zobaczyć strongę główną na której znajduje się między innymi instrukcja jak uruchomić API.
Kreator zapytań ani same zapytania do API nie będą działać jeśli nie będzie uruchomionego API!

## Gdzie się znajdują rzeczy z poleceń?
1. Szkielet - strona http://127.0.0.1:8000/
2. Kreator zapytań - strona http://127.0.0.1:8000/request_builder. Do kreatora zapytań można też przejść ze strony głównej
Link jest zawarty w podsekcji oznaczonej jako "nowość"
3. Wykresy - wystarczy w kreatorze zapytań zaznaczyć opcję "Wyświetl wynik zapytania w postaci wykresu".
