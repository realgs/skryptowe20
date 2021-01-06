import React, {useEffect, useRef, useState} from 'react';
import ReactApexCharts from 'react-apexcharts'

export default function ApiDocs() {
    return (<>
            <h2 className="pt-2">Exchange API Docs</h2>
            <div className="p-3">
                <div className="row row-cols-1 row-cols-md-2 g-4">
                    <div className="col">
                        <div className="card shadow">
                            <h5 className="card-header"><strong>Wymagane programy:</strong></h5>
                            <div className="card-text">
                                <ul className="list-group">
                                    <li className="list-group-item">python3</li>
                                    <li className="list-group-item">npm</li>
                                    <li className="list-group-item">node.js</li>
                                    <li className="list-group-item">docker</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div className="col">
                        <div className="card shadow">
                            <h5 className="card-header"><strong>Wymagane paczki python:</strong></h5>
                            <div className="card-text">
                                <ul className="list-group">
                                    <li className="list-group-item">flask</li>
                                    <li className="list-group-item">flask_cors</li>
                                    <li className="list-group-item">flask_limiter</li>
                                    <li className="list-group-item">psycopg2</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="text-start">
                    <h4 className="pt-2 mt-3 mb-3">Instrukcja uruchomienia:</h4>
                    <ul className="list-group shadow">
                        <li className="list-group-item"><strong>1.)</strong> Przechodzimy do katalogu lab6</li>
                        <li className="list-group-item"><strong>2.)</strong> Uruchamiamy aplikacje komendą
                            'docker-compose up'
                        </li>
                        <li className="list-group-item"><strong>3.)</strong> Przechodzimy do przeglądarki</li>
                        <li className="list-group-item"><strong>4.)</strong> Wchodzimy na stronę znajdującą się pod
                            adresem:
                            'localhost:3000'
                        </li>
                    </ul>
                    <h4 className="pt-2 mt-3 mb-3">Endpointy:</h4>
                    <div className="shadow card p-2">
                        <h5><strong>Kursy waluty: /api/rates/$currency_codes</strong></h5>
                        <ul className="list-group">
                            <li className="list-group-item list-group-item-secondary"><strong>Parametry
                                zapytania:</strong></li>
                            <li className="list-group-item"><strong>$currency_code</strong> - kod waluty dla
                                oczkiwanych rat (
                                Wspierane waluty: EUR, USD, CHF, GBP, TRY, AUD, RUB )
                            </li>
                        </ul>
                        <ul className="list-group mt-2">
                            <li className="list-group-item list-group-item-secondary"><strong>Parametry
                                ścieżki</strong></li>
                            <li className="list-group-item"><strong>startDate</strong> - data początowa rat (np.
                                2020-11-22)
                            </li>
                            <li className="list-group-item"><strong>endDate</strong> - data końcowa rat (np.
                                2020-11-28)
                            </li>
                        </ul>
                        <ul className="list-group mt-2">
                            <li className="list-group-item list-group-item-secondary"><strong>Przykładowe
                                zapytania</strong></li>
                            <li className="list-group-item"><a className="link-info"
                                                               href="http://localhost:8080/api/rates/USD?startDate=2020-11-22&endDate=2020-11-28">http://localhost:8080/api/rates/USD?startDate=2020-11-22&endDate=2020-11-28</a>
                            </li>
                            <li className="list-group-item"><a className="link-info"
                                                               href="http://localhost:8080/api/rates/EUR?startDate=2019-02-22&endDate=2019-05-01">http://localhost:8080/api/rates/EUR?startDate=2019-02-22&endDate=2019-05-01</a>
                            </li>
                        </ul>
                    </div>
                    <div className="shadow card p-2 mt-3">
                        <h5><strong>Dane sprzedaży: /api/sales/$currency_code</strong></h5>
                        <ul className="list-group">
                            <li className="list-group-item list-group-item-secondary"><strong>Parametry
                                zapytania:</strong></li>
                            <li className="list-group-item"><strong>$currency_code</strong> - kod waluty dla
                                oczkiwanych rat (
                                Wspierane waluty: EUR, USD, CHF, GBP, TRY, AUD, RUB )
                            </li>
                        </ul>
                        <ul className="list-group mt-2">
                            <li className="list-group-item list-group-item-secondary"><strong>Parametry
                                ścieżki</strong></li>
                            <li className="list-group-item"><strong>startDate</strong> - dzień, dla którego
                                podsumowujemy sprzedaż (np. 2020-11-22)
                            </li>
                        </ul>
                        <ul className="list-group mt-2">
                            <li className="list-group-item list-group-item-secondary"><strong>Przykładowe
                                zapytania</strong></li>
                            <li className="list-group-item"><a className="link-info"
                                                               href="http://localhost:8080/api/sales/USD?date=2019-03-10">http://localhost:8080/api/sales/USD?date=2019-03-10</a>
                            </li>
                            <li className="list-group-item"><a className="link-info"
                                                               href="http://localhost:8080/api/sales/EUR?date=2019-02-22">http://localhost:8080/api/sales/EUR?date=2019-02-22</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </>
    );
}
