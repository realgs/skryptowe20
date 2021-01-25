<template>
    <div>
        <div>
            <h1>Exchange rates and sales API</h1>
            <p>
                This API provides the data of USD
                to PLN exchange rates and daily sales in both USD and PLN from Northwind
                sample database.
            </p>
            <p>
                You can test the data provided by the API by
                <a href="/request"><span class="green">making a request</span></a>.
            </p>
        </div>

        <div class="points">
            <h2>Data sources</h2>
            <p>
                Sales database is a version of the Microsoft Access 2000 Northwind sample database,
                re-engineered for SQLite3 - <a href="https://github.com/jpwhite3/northwind-SQLite3">
                    <span class="green">https://github.com/jpwhite3/northwind-SQLite3</span>
                </a>.
                This database is extended by tables ExchangeRate and TotalSales. USD to PLN exchange
                rates come from here - <a href="http://api.nbp.pl/">
                    <span class="green">
                        http://api.nbp.pl/
                    </span>
                </a>.
            </p>
            <h2>Limits</h2>
            <ul>
                <li>
                    Available dates for the exchange rates range from <span class="bold">2002-01-02</span>
                    to <span class="bold">today</span>.
                </li>
                <li>
                    Available dates for the sales range from <span class="bold">2012-07-04</span> to
                    <span class="bold">2016-02-19</span>.
                </li>
                <li>
                    <span class="bold">YYYY-MM-DD</span> is the only acceptable date formatting.
                </li>
                <li>
                    There is a request limit that allows 20 request per minute of every request type.
                </li>
                <li>
                    There is a cache timeout set for 100s.
                </li>
            </ul>
            <h2>Usage</h2>
            <ul>
                <li>
                    USD to PLN exchange rate at date: <span class="bold">http://127.0.0.1:5000/api/rates/USD/{date}</span>
                    <ul>
                        <li>example: http://127.0.0.1:5000/api/rates/USD/2020-02-20</li>
                    </ul>
                </li>
                <li>
                    USD to PLN exchange rate from the start_date to end_date: <span class="bold">http://127.0.0.1:5000/api/rates/USD/{start_date}/{end_date}</span>
                    <ul>
                        <li>example: http://127.0.0.1:5000/api/rates/USD/2013-04-07/2014-10-22</li>
                    </ul>
                </li>
                <li>
                    sales data at date: <span class="bold">http://127.0.0.1:5000/api/sales/{date}</span>
                    <ul>
                        <li>example: http://127.0.0.1:5000/api/sales/2013-01-01</li>
                    </ul>
                </li>
                <li>
                    sales data from start_date to end_date: <span class="bold">http://127.0.0.1:5000/api/sales/{start_date}/{end_date}</span>
                    <ul>
                        <li>example: http://127.0.0.1:5000/api/sales/2013-04-07/2014-10-22</li>
                    </ul>
                </li>
                <p>Alternatively, instead of 127.0.0.1, you could use localhost, those are the same</p>
            </ul>
            <h2>Errors</h2>
            <ul>
                <li>
                    <span class="bold">400</span> - Occurs when given date is out of available range.
                </li>
                <li>
                    <span class="bold">404</span> - Occurs when the API url is incorrect.
                </li>
                <li>
                    <span class="bold">416</span> - Occurs when range given in the URL is not satisfiable.
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Home",
    };
</script>

<style scoped>
    h2 {
        margin: 40px 0 15px;
    }

    h4 {
        margin: 30px 0 30px;
    }

    li {
        margin: 7px;
    }

    .bold {
        font-weight: bold;
    }

    .green {
        color: #42b983;
    }

    .points {
        text-align: justify;
        margin: 0 20% 0 20%;
    }
</style>