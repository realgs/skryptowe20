import React from 'react';
import {Container,Row,Col} from 'react-bootstrap'
import './Styles.css'


function Home() {
  return (
    <div>
        <Container>
            <Row>
            <Col xs={8}><HomeContext /></Col>
            </Row>
        </Container>
    </div>
  );
}

function HomeContext() {
    return (
        <div>
            <br />
            <h1 class="title">Rates and Sales API</h1>
            <h3 class="subtitle">Jakub Smołka - 246987</h3>
            <br/><br/>

            <h4 class="header">Jak uzyskać notowania</h4>
            <p>Notowania z konkretnego dnia lub zakresu dat wraz z informacją <b>'interpolated'</b>:</p>
            <p id="url"><span class="type">GET </span>
                https://rates-and-sales-api.herokuapp.com/api/rates/<span class="type">[waluta]</span>/<span class="param">[data]</span> <br/> 
                <span class="type">GET </span>
                    https://rates-and-sales-api.herokuapp.com/api/rates/<span class="type">[waluta]</span>/<span class="param">[data_od]</span>/<span class="param">[data_do]</span> </p>
            <p><b>Na przykład:</b> 
                <span class="type">GET</span> https://rates-and-sales-api.herokuapp.com/api/rates/<span class="type">USD</span>/<span class="param">2007-02-16</span>/<span class="param">2007-06-06</span> </p>
            <br/>

            <h4 class="header">Jak uzyskać sumę sprzedaży</h4>
            <p>Suma sprzedaży wraz z przeliczeniem po kursie z danego dnia, lub zakresu dat:</p>
            <p id="url"><span class="type">GET </span> 
                    http://127.0.0.1:5000/api/sales/<span class="type">sales</span>/<span class="param">[data]</span> <br/> 
                <span class="type">GET </span> 
                    http://127.0.0.1:5000/api/sales/<span class="type">sales</span>/<span class="param">[data_od]</span>/<span class="param">[data_do]</span> </p>
            <p><b>Na przykład:</b>
                <span class="type">GET </span> 
                    http://127.0.0.1:5000/api/sales/<span class="type">sales</span>/<span class="param">2007-02-16</span>/<span class="param">2007-06-06</span> </p>
            <br/>

            <h4 class="header">Cache</h4>
            <p>W zadaniu zaimplementowałem bardzo prosty system cache'u, 
                który sprawdza czy zapytanie użytkownika zostało wykonane 
                wcześniej i jeśli tak, to zwraca zapamiętaną wcześniej wartość. 
                W przeciwnym wypadku zapamiętuje odpowiedź na zapytanie użytkownika w słowniku.
                <br/><br/>Cache odświeża się co ok. <b>24 godziny</b>.
            </p>

            <br/>

            <h4 class="header">Limity</h4>
            <p>Limity są nałożone na adres sieciowy użytkownika i mają następujące ograniczenia:</p>
            <ul>
                <li>Zapytania o notowania: <b>10 na minutę</b></li>
                <li>Zapytania o sprzedaż z konkretnego dnia: <b>50 na minutę</b></li>
                <li>Zapytania o sprzedaż z zakresu dat: <b>10 na minutę</b> (do testów)</li>
            </ul>
            <p>Odpowiedzią na przekroczony limit zapytań jest kod błędu <b>429</b>.</p>
            <br/><br/>
        </div>
    )
    
}



export default Home;