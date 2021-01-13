import React, {Component} from 'react';
import './Home.css'

class HomeComponent extends Component {
    render() {
        return (
            instruction
        );
    }
}

const instruction =
    <React.Fragment>
        <main className="container">
            <h1>Instrukcja uruchomienia</h1>
            <div>
                Przed uruchomieniem programu należy posiadać na komputerze program python3 oraz mieć do niego paczki:
                <ul>
                    <li>flask</li>
                    <li>flask_limitter</li>
                    <li>flask-cors</li>
                    <li>sqlite3</li>
                    <li>requests</li>
                </ul>
                A także Node.js oraz pakiet npm.
            </div>
            <p>
                Aby uruchomić program wystarczy zaciągnąć pliki na dysk oraz posiadać bazę danych wykorzystywaną
                w zadaniu.
            </p>
            <p>
                Aby uruchomić aplikację, za pierwszym razem uruchamiamy skrypt main.py, aby zainicjować i wypełnić
                bazę damnych brakującymi tabelami.
            </p>
            <p>
                Gdy mamy bazę danych należy uruchomić skrypt myAPI.py, który uruchomi serwer oczekujący na zapytania.
            </p>
            <p>
                Następnie należy przejść do folderu currency-api-front-end i wykonać komendy:
                <b>npm install</b> oraz <b>npm start</b>
            </p>
            <p>
                Aby korzystać z aplikacji bez interfejsu graficznego należy udać się na stronę http://127.0.0.1:5000/
                (nie trzeba wtedy używać komendy npm install oraz npm start) i używać zapytań przedstawionych w sekcji
                <b> Zaimplementowane endpointy</b>.
            </p>
            <p>
                Jeśli jednak zdecydujemy się korzystać z frontendu należy wejść na stronę http://localhost:3000/
                aby zacząć korzystać z interfejsu graficznego.
            </p>
            <br/>
            <h1>Zaimplementowane endpointy</h1>
            <ul>
                <li>
                    <b>/api/rates/fordate?date=value</b>
                    <ul>
                        <li>
                            zapytanie GET zwraca nam kurs waluty USD w przeliczeniu na PLN na dany dzień podany w
                            parametrze
                            value
                        </li>
                    </ul>
                </li>
                <li>
                    <b>/api/rates/fordatespan?from=value1&to=value2</b>
                    <ul>
                        <li>
                            zapytanie GET zwraca kursy waluty US w przeliczeniu na PLN dla przedziału dni podanych w
                            parametrach
                            od value1 do value2
                        </li>
                    </ul>
                </li>
                <li>
                    <b>/api/sales/fordate?date=value</b>
                    <ul>
                        <li>
                            zapytanie GET zwraca łączną sumę sprzedaży w walucie PLN oraz USD dla dnia podanego jako
                            value
                        </li>
                    </ul>
                </li>
                <li>
                    <b>/api/sales/fordatespan?from=value1&to=value2</b>
                    <ul>
                        <li>
                            zapytanie GET zwraca łączną sumę sprzedaży walucie PLN oraz USD dla przedziału dni podanych
                            w parametrach
                            od value1 do value2
                        </li>
                    </ul>
                </li>

            </ul>
            <h1>Zwracane kody</h1>
            <ul>
                <li>200 -> success</li>
                <li>401 -> błąd po stronie klienta, np niepoprawne dane lub ich brak</li>
                <li>501 -> błąd po stronie serwera, np. nie znaleziono danych w bazie danych</li>
            </ul>
            <h1>Limity</h1>
            <ul>
                <li>
                    Limity są przypisane po IP użytkownika, który wysyła zapytanie.
                </li>
                <li>
                    Podstawowy limit requestów jakie możemy wykonać to 300 na dzień.
                </li>
                <li>
                    Zapytanie o wartość dolara w PLN dla konkretnego dnia możemy wykonać nie częściej niż 15 razy na
                    minutę i nie częściej niż 100 razy na godzinę.
                </li>
                <li>
                    Zapytanie o wartości dolara w PLN dla przedziału dat możemy wykonać nie częściej niż 5 razy na
                    minutę i nie częściej niż 70 razy na godzinę.
                </li>
                <li>
                    Zapytanie o wartości sprzedaży w PLN i USD w danym dniu możemy wykonać nie częściej niż 10 razy na
                    minutę i nie częściej niż 90 razy na godzinę.
                </li>
            </ul>
            <p>
                Kreator: Damian Żółtowski - 246651
            </p>
        </main>
    </React.Fragment>

export default HomeComponent;
