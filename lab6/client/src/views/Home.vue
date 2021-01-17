<template>
  <div class="home">
    <h1 id="lab-api">Laboratorium Skryptowe - API</h1>
    <hr />
    <div id="spis-tresci">
      <h2>Spis treści</h2>
      <ul>
        <li><a href="#ogolne-informacje">Ogólne informacje</a></li>
        <li><a href="#technologie">Technologie</a></li>
        <li>
          <a href="#instalacja">Instalacja</a>
          <ul>
            <li><a href="#konfiguracja">Konfiguracja</a></li>
            <li><a href="#uruchomienie">Uruchomienie</a></li>
          </ul>
        </li>
        <li><a href="#funkcjonalnosci">Funkcjonalności</a></li>
        <li>
          <a href="#sposob-uzycia">Sposób użycia</a>
          <ul>
            <li><a href="#format">Format</a></li>
            <li><a href="#parametry-zapytan">Parametry zapytań</a></li>
            <li><a href="#opcjonalne-parametry">Opcjonalne parametry</a></li>
            <li>
              <a href="#adresacja-api">Adresacja API</a>
              <ul>
                <li>
                  <a href="#notowanie-z-danego-dnia">Notowanie z danego dnia</a>
                </li>
                <li>
                  <a href="#notowania-z-danego-okresu"
                    >Notowania z danego okresu</a
                  >
                </li>
                <li>
                  <a href="#notowania-z-calego-okresu"
                    >Notowania z całego okresu</a
                  >
                </li>
                <li>
                  <a href="#suma-sprzedazy">Suma sprzedaży z danego dnia</a>
                </li>
              </ul>
            </li>
            <li><a href="#wyjatki">Wyjątki</a></li>
          </ul>
        </li>
        <li>
          <a href="#inne">Inne</a>
          <ul>
            <li><a href="#struktura-bazy-danych">Struktura bazy danych</a></li>
          </ul>
        </li>
      </ul>
    </div>
    <hr />
    <h2 id="ogolne-informacje">Ogólne informacje</h2>
    <p>
      API oparte na frameworku Flask służące do pobierania danych o
      historycznych kursach walut oraz sumie sprzedaży w danym dniu przeliczonej
      po kursie z danego dnia.
    </p>
    <hr />
    <h2 id="technologie">Technologie</h2>
    <p>Wykorzystane technologie wymagane do uruchomienia projektu:</p>
    <ul>
      <li>Python - 3.8</li>
      <li>Flask - 1.1.2</li>
      <li>Flask-Caching - 1.9.0</li>
      <li>Flask-Limiter - 1.4</li>
    </ul>
    <hr />
    <h2 id="instalacja">Instalacja</h2>
    <p>
      Przed uruchomieniem aplikacji niezbędna jest instalacja wymienionych
      technologii na maszynie, na której serwer ma działać.
    </p>
    <hr />
    <h3 id="konfiguracja">Konfiguracja</h3>
    <p>
      Zanim uruchomi się aplikację powinno się ją najpierw skonfigurować. Aby to
      zrobić należy edytować plik: <code>config.py</code>
    </p>
    <p><strong>Dostępne opcje:</strong></p>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Opcja</th>
          <th style="text-align: center">Możliwe wartości</th>
          <th style="text-align: center">Wartość domyślna</th>
          <th style="text-align: right">Opis</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>DATABASE_FILE_PATH</td>
          <td style="text-align: center"><code>filepath: string</code></td>
          <td style="text-align: center">
            <code>&#39;database.sqlite&#39;</code>
          </td>
          <td style="text-align: right">
            Ścieżka do pliku bazy danych sqlite3
          </td>
        </tr>
        <tr>
          <td>DEBUG_MODE</td>
          <td style="text-align: center">
            <code>True</code> <code>False</code>
          </td>
          <td style="text-align: center"><code>False</code></td>
          <td style="text-align: right">Tryb debugowania</td>
        </tr>
        <tr>
          <td>ENABLE_LIMITER</td>
          <td style="text-align: center">
            <code>True</code> <code>False</code>
          </td>
          <td style="text-align: center"><code>True</code></td>
          <td style="text-align: right">
            Aktywuje zapezpieczenie przed zbyt częstymi zapytaniami dla
            poszczególnych użytkowników (rozpoznawanie po zewnętrznym adresie IP
            klienta)
          </td>
        </tr>
        <tr>
          <td>INDEX_LIMIT</td>
          <td style="text-align: center"><code>limit: string</code></td>
          <td style="text-align: center">
            <code>&#39;10000 per hour&#39;</code>
          </td>
          <td style="text-align: right">Limit zapytań dla strony domowej</td>
        </tr>
        <tr>
          <td>GET_RATES_ALL_LIMIT</td>
          <td style="text-align: center"><code>limit: string</code></td>
          <td style="text-align: center">
            <code>&#39;5 per minute;50 per hour&#39;</code>
          </td>
          <td style="text-align: right">
            Limit zapytań dla listy wszystkich kursów waluty
          </td>
        </tr>
        <tr>
          <td>GET_RATE_DAY_LIMIT</td>
          <td style="text-align: center"><code>limit: string</code></td>
          <td style="text-align: center">
            <code>&#39;100 per minute;1000 per hour&#39;</code>
          </td>
          <td style="text-align: right">
            Limit zapytań dla notowania waluty z danego dnia
          </td>
        </tr>
        <tr>
          <td>GET_RATES_RANGE_LIMIT</td>
          <td style="text-align: center"><code>limit: string</code></td>
          <td style="text-align: center">
            <code>&#39;10 per minute;100 per hour&#39;</code>
          </td>
          <td style="text-align: right">
            Limit zapytań dla notowań waluty z danego zakresu
          </td>
        </tr>
        <tr>
          <td>GET_SALES_SUM_DAY_LIMIT</td>
          <td style="text-align: center"><code>limit: string</code></td>
          <td style="text-align: center">
            <code>&#39;100 per minute;1000 per hour&#39;</code>
          </td>
          <td style="text-align: right">
            Limit zapytań dla sumy sprzedaży z danego dnia
          </td>
        </tr>
      </tbody>
    </table>
    <p>
      Notacja limitów zapytań jest dostępna w
      <a
        href="https://flask-limiter.readthedocs.io/en/stable/#rate-limit-string-notation"
        >dokumentacji Flask-Limiter</a
      >.
    </p>
    <hr />
    <h3 id="uruchomienie">Uruchomienie</h3>
    <ol>
      <li>W terminalu przejdź do folderu projektu:</li>
    </ol>
    <pre><code>$ <span class="hljs-built_in">cd</span> lab5-api/
</code></pre>
    <ol>
      <li>
        Uruchom aplikację:
        <ul>
          <li>
            w trybie lokalnym (<code>host=127.0.0.1</code>):
            <pre><code>$ flask <span class="hljs-keyword">run</span><span class="bash"></span>
</code></pre>
          </li>
          <li>
            wykorzystująć jako adres hosta IP urządzenia:
            <pre><code>$ flask run --host=<span class="hljs-number">0.0.0.0</span>
</code></pre>
          </li>
        </ul>
      </li>
    </ol>
    <hr />
    <h2 id="funkcjonalnosci">Funkcjonalności</h2>
    <ul>
      <li>Pobieranie historycznych notowań walut z danego dnia</li>
      <li>Pobieranie historycznych notowań walut z wybranego okresu</li>
      <li>
        Pobieranie sumarycznej sprzedaży z danego dnia w walucie oryginalnej
        <em>USD</em> i po przeliczeniu na <em>PLN</em>
      </li>
    </ul>
    <hr />
    <h2 id="sposob-uzycia">Sposób użycia</h2>
    <p>W tej sekcji znajdują się informacje o sposobie korzystania z API.</p>
    <hr />
    <h3 id="format">Format</h3>
    <p>
      Dane zwracane są w formacie <code>JSON</code>. Wartości notowań (sekcja
      <code>rates</code>) są podawane w walucie <code>PLN</code> - polski złoty.
    </p>
    <hr />
    <h3 id="parametry-zapytan">Parametry zapytań</h3>
    <ul>
      <li>
        <code>{currency_code}</code> - trzyliterowy kod waluty, np.
        <code>USD</code>,<code>EUR</code>
      </li>
      <li><code>{date}</code> - data w formacie <code>RRRR-MM-DD</code></li>
      <li>
        <code>{start_date}</code> - data początku okresu w formacie
        <code>RRRR-MM-DD</code>
      </li>
      <li>
        <code>{end_date}</code>- data końca okresu w formacie
        <code>RRRR-MM-DD</code>
      </li>
    </ul>
    <hr />
    <h3 id="opcjonalne-parametry">Opcjonalne parametry</h3>
    <p>Parametry podawane na końcu zapytania po znaku <code>$</code></p>
    <ul>
      <li>
        <code>interpolated</code> - interpolated jest ustawione na
        <code>1</code> dla dni, które swoją wartość przybrały jako tę z
        poprzedzającego dnia posiadającego notowanie. <code>0</code> w
        przeciwnym przypadku. Przykład poprawnego zapisu:
        <code>?interpolated=1</code>
      </li>
    </ul>
    <hr />
    <h3 id="adresacja-api">Adresacja API</h3>
    <h4 id="notowanie-z-danego-dnia">Notowanie z danego dnia</h4>
    <p>
      <code
        >http://host:5000/api/v1/rates/{currency_code}/day/{date}?interpolated=[0,1]</code
      >
    </p>
    <p>Przykład zwracanych danych:</p>
    <p><code>http://host:5000/api/v1/rates/eur/day/2011-01-01</code></p>
    <pre><code>{}
</code></pre>
    <p>
      Standardowo zwracane są notowania z polem
      <code>&quot;interpolated&quot;: 0</code>, czyli takie, które nie zostały
      sztucznie wygenerowane. W takim wypadku jeżeli wybrany zostanie dzień, w
      którym banki nie prowadziły notowań to zostanie zwrócony pusty słownik. W
      celu uwzględnienia w zapytaniu notowań wygenerowanych sztucznie należy
      zastosować opcjonalny argument <code>interpolated</code> w ciele
      zapytania. Poniżej jest przykład jego zastosowania:
    </p>
    <p>
      <code
        >http://host:5000/api/v1/rates/eur/day/2011-01-01?interpolated=1</code
      >
    </p>
    <pre><code>{
  <span class="hljs-attr">"code"</span>: <span class="hljs-string">"EUR"</span>,
  <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2011-01-01"</span>,
  <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">1</span>,
  <span class="hljs-attr">"rate"</span>: <span class="hljs-number">3.9603</span>
}
</code></pre>
    <p>
      Te działanie jest właściwe dla wszystkich zapytań dotyczących notowań
      walut.
    </p>
    <hr />
    <h4 id="notowania-z-danego-okresu">Notowania z danego okresu</h4>
    <p>
      <code
        >http://host:5000/api/v1/rates/{currency_code}/range/{start_date}/{end_date}?interpolated=[0,1]</code
      >
    </p>
    <p>Przykład zwracanych danych:</p>
    <p>
      <code>http://host:5000/api/v1/rates/usd/range/2010-01-01/2010-01-06</code>
    </p>
    <pre><code>[
  {
    <span class="hljs-attr">"code"</span>: <span class="hljs-string">"USD"</span>,
    <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2010-01-04"</span>,
    <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">0</span>,
    <span class="hljs-attr">"rate"</span>: <span class="hljs-number">2.8465</span>
  },
  {
    <span class="hljs-attr">"code"</span>: <span class="hljs-string">"USD"</span>,
    <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2010-01-05"</span>,
    <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">0</span>,
    <span class="hljs-attr">"rate"</span>: <span class="hljs-number">2.8264</span>
  },
  {
    <span class="hljs-attr">"code"</span>: <span class="hljs-string">"USD"</span>,
    <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2010-01-06"</span>,
    <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">0</span>,
    <span class="hljs-attr">"rate"</span>: <span class="hljs-number">2.8493</span>
  }
]
</code></pre>
    <p>
      <code
        >http://host:5000/api/v1/rates/usd/range/2010-01-01/2010-01-04?interpolated=1</code
      >
    </p>
    <pre><code>[
  {
    <span class="hljs-attr">"code"</span>: <span class="hljs-string">"USD"</span>,
    <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2010-01-01"</span>,
    <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">1</span>,
    <span class="hljs-attr">"rate"</span>: <span class="hljs-number">2.8503</span>
  },
  {
    <span class="hljs-attr">"code"</span>: <span class="hljs-string">"USD"</span>,
    <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2010-01-02"</span>,
    <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">1</span>,
    <span class="hljs-attr">"rate"</span>: <span class="hljs-number">2.8503</span>
  },
  {
    <span class="hljs-attr">"code"</span>: <span class="hljs-string">"USD"</span>,
    <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2010-01-03"</span>,
    <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">1</span>,
    <span class="hljs-attr">"rate"</span>: <span class="hljs-number">2.8503</span>
  },
  {
    <span class="hljs-attr">"code"</span>: <span class="hljs-string">"USD"</span>,
    <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2010-01-04"</span>,
    <span class="hljs-attr">"interpolated"</span>: <span class="hljs-number">0</span>,
    <span class="hljs-attr">"rate"</span>: <span class="hljs-number">2.8465</span>
  }
]
</code></pre>
    <hr />
    <h4 id="notowania-z-calego-okresu">Notowania z całego okresu</h4>
    <p>
      <code
        >http://host:5000/api/v1/rates/{currency_code}/all?interpolated=[0,1]</code
      >
    </p>
    <hr />
    <h4 id="suma-sprzedazy">Suma sprzedaży z danego dnia</h4>
    <p><code>http://host:5000/api/v1/sales/sum/{date}</code></p>
    <p>
      Waluta oryginalna to <code>USD</code>, waluta po przeliczeniu to
      <code>PLN</code>.
    </p>
    <p>Przykład zwracanych danych:</p>
    <p><code>http://host:5000/api/v1/sales/sum/2014-04-28</code></p>
    <pre><code>{
  <span class="hljs-attr">"date"</span>: <span class="hljs-string">"2014-04-28"</span>,
  <span class="hljs-attr">"exchange_rate"</span>: <span class="hljs-number">3.0368</span>,
  <span class="hljs-attr">"exchanged_value"</span>: <span class="hljs-number">7830.32</span>,
  <span class="hljs-attr">"original_value"</span>: <span class="hljs-number">2578.48</span>
}
</code></pre>
    <hr />
    <h3 id="wyjatki">Wyjątki</h3>
    <p>
      Podczas korzystania z API mogą wystąpić wyjątki spowodowane podaniem
      nieprawidłowych parametrów lub niepoprawnego działania serwera. Rezultatem
      jest odpowiedź w formacie <code>JSON</code> z dwoma polami
      <code>error</code> i <code>message</code>.
    </p>
    <p>Przykładowa wiadomość o wystąpieniu wyjątku:</p>
    <pre><code>{
  <span class="hljs-attr">"error"</span>: <span class="hljs-string">"CurrencyCodeError"</span>,
  <span class="hljs-attr">"message"</span>: <span class="hljs-string">
    "Invalid currency code. Valid code should consist of 3 letters"</span>
}
</code></pre>
    <strong>Zdefiniowane wyjątki</strong>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Nazwa <code>error</code></th>
          <th style="text-align: left">Wiadomość <code>message</code></th>
          <th style="text-align: right">Kod HTML</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>DateFormatError</td>
          <td style="text-align: left">
            Invalid date argument. Date has to be passed in given format:
            YYYY-MM-DD
          </td>
          <td style="text-align: right">422</td>
        </tr>
        <tr>
          <td>RangeOrderError</td>
          <td style="text-align: left">
            Dates are in wrong order. End date must be after/equal start date.
          </td>
          <td style="text-align: right">422</td>
        </tr>
        <tr>
          <td>OutOfRangeError</td>
          <td style="text-align: left">
            Requested range exceedes the maximum range available in database.
          </td>
          <td style="text-align: right">422</td>
        </tr>
        <tr>
          <td>CurrencyCodeError</td>
          <td style="text-align: left">
            Invalid currency code. Valid code should consist of 3 letters
          </td>
          <td style="text-align: right">422</td>
        </tr>
        <tr>
          <td>NoCurrencyError</td>
          <td style="text-align: left">
            Requested currency is not available in database.
          </td>
          <td style="text-align: right">422</td>
        </tr>
        <tr>
          <td>InterpolatedParamError</td>
          <td style="text-align: left">
            Invalid argument value - interpolated should be set as 0 or 1
          </td>
          <td style="text-align: right">422</td>
        </tr>
        <tr>
          <td>NoSalesError</td>
          <td style="text-align: left">There were no sales on given day</td>
          <td style="text-align: right">422</td>
        </tr>
        <tr>
          <td>InternalServerError</td>
          <td style="text-align: left">500 Internal Server Error</td>
          <td style="text-align: right">500</td>
        </tr>
        <tr>
          <td>DatabaseError</td>
          <td style="text-align: left">
            Database connection failed. Please contact server administrator.
          </td>
          <td style="text-align: right">500</td>
        </tr>
      </tbody>
    </table>

    <hr />
    <h2 id="inne">Inne</h2>
    <p>
      W dostarczonej bazie danych dane o notowań walut zawierają się w zakresie
      <code>2010-01-01</code> - <code>2020-12-19</code>.
    </p>
    <p>
      Dane o sprzedaży zawarte są w zakresie <code>2014-01-03</code> -
      <code>2017-12-30</code>.
    </p>
    <p>
      Dostępne waluty: <code>USD</code>, <code>THB</code>, <code>AUD</code>,
      <code>HKD</code>, <code>CAD</code>, <code>NZD</code>, <code>EUR</code>,
      <code>JPY</code>, <code>GBP</code>, <code>CHF</code>.
    </p>
    <hr />
    <h3 id="struktura-bazy-danych">Struktura bazy danych</h3>
    <p>
      Struktura wykorzystywanej bazy danych w pliku
      <code>database.sqlite</code>.
    </p>
    <ul>
      <li><strong>Currencies</strong>(<ins>code</ins>)</li>
      <li><strong>Customers</strong>(<ins>id</ins>, name)</li>
      <li>
        <strong>Orders</strong>(<ins>row_id</ins>, order_id, order_date,
        #customer_id, #product_id, value)
      </li>
      <li><strong>Products</strong>(<ins>id</ins>, name)</li>
      <li>
        <strong>Rates</strong>(<ins>#code, date</ins>, rate, interpolated)
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Home',
  props: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  line-height: 1.25;
}

#spis-tresci li {
  font-weight: bolder;
}

#spis-tresci li > ul > li {
  font-weight: normal;
}

tbody > tr > td > code {
  background-color: #f7f7f7;
}

code {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: #f2f2f2;
  border-radius: 6px;
  color: black;
}

pre {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f5f7f7;
  border-radius: 6px;
}

pre > code {
  background-color: #f5f7f7;
}

a {
  color: #42b983;
  text-decoration-line: none;
}
</style>
