# SampleSales - API - Frontend

## Ogólne informacje

### Konfiguracja projektu

Zanim uruchomi się aplikację powinno się ją najpierw skonfigurować. Aby to zrobić należy edytować plik: `client/config.js` oraz `server/config.py` i ustawić tam odpowiednio adresy to odwoływania się do serwera front i backendu. Standardowo projekt jest skonfigurowany pod działania lokalne.

### Uruchomienie

1. W terminalu przejdź do folderu projektu:

```
$ cd lab6/
```

2. Uruchom serwer frontendu:

```
$ cd client/
$ npm run serve
```

3. Uruchom serwer backendu:

```
 $ cd server/
 $ flask run
```

# API

## Spis treści

- [Ogólne informacje](#ogólne-informacje)
- [Technologie](#technologie)
- [Instalacja](#instalacja)
  - [Konfiguracja](#konfiguracja)
- [Funkcjonalności](#funkcjonalności)
- [Sposób użycia](#sposób-użycia)
  - [Format](#format)
  - [Parametry zapytań](#parametry-zapytań)
  - [Opcjonalne parametry](#opcjonalne-parametry)
  - [Adresacja API](#adresacja-api)
    - [Notowanie z danego dnia](#notowanie-z-danego-dnia)
    - [Notowania z danego okresu](#notowania-z-danego-okresu)
    - [Notowania z całego okresu](#notowania-z-całego-okresu)
    - [Suma sprzedaży z danego dnia](#suma-sprzedaży-z-danego-dnia)
  - [Wyjątki](#wyjątki)
- [Inne](#inne)
  - [Struktura bazy danych](#struktura-bazy-danych)

## Ogólne informacje

API oparte na frameworku Flask służące do pobierania danych o historycznych kursach walut oraz sumie sprzedaży w danym dniu przeliczonej po kursie z danego dnia.

## Technologie

Wykorzystane technologie wymagane do uruchomienia projektu:

- Python - 3.8
- Flask - 1.1.2
- Flask-Caching - 1.9.0
- Flask-Limiter - 1.4

## Instalacja

Przed uruchomieniem aplikacji niezbędna jest instalacja wymienionych technologii na maszynie, na której serwer ma działać.

### Konfiguracja

Zanim uruchomi się aplikację powinno się ją najpierw skonfigurować. Aby to zrobić należy edytować plik: `config.py`

**Dostępne opcje:**

| Opcja                   |  Możliwe wartości  |         Wartość domyślna         |                                                                                                                                      Opis |
| ----------------------- | :----------------: | :------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------: |
| DATABASE_FILE_PATH      | `filepath: string` |       `'database.sqlite'`        |                                                                                                     Ścieżka do pliku bazdy danych sqlite3 |
| DEBUG_MODE              |   `True` `False`   |             `False`              |                                                                                                                          Tryb debugowania |
| ENABLE_LIMITER          |   `True` `False`   |              `True`              | Aktywuje zapezpieczenie przed zbyt częstymi zapytaniami dla poszczególnych użytkowników (rozpoznawanie po zewnętrznym adresie IP klienta) |
| INDEX_LIMIT             |  `limit: string`   |        `'10000 per hour'`        |                                                                                                          Limit zapytań dla strony domowej |
| GET_RATES_ALL_LIMIT     |  `limit: string`   |   `'5 per minute;50 per hour'`   |                                                                                          Limit zapytań dla listy wszystkich kursów waluty |
| GET_RATE_DAY_LIMIT      |  `limit: string`   | `'100 per minute;1000 per hour'` |                                                                                          Limit zapytań dla notowania waluty z danego dnia |
| GET_RATES_RANGE_LIMIT   |  `limit: string`   |  `'10 per minute;100 per hour'`  |                                                                                         Limit zapytań dla notowań waluty z danego zakresu |
| GET_SALES_SUM_DAY_LIMIT |  `limit: string`   | `'100 per minute;1000 per hour'` |                                                                                            Limit zapytań dla sumy sprzedaży z danego dnia |

Notacja limitów zapytań jest dostępna w [dokumentacji Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/#rate-limit-string-notation).

## Funkcjonalności

- Pobieranie historycznych notowań walut z danego dnia
- Pobieranie historycznych notowań walut z wybranego okresu
- Pobieranie sumarycznej sprzedaży z danego dnia w walucie oryginalnej _USD_ i po przeliczeniu na _PLN_

## Sposób użycia

W tej sekcji znajdują się informacje o sposobie korzystania z API.

### Format

Dane zwracane są w formacie `JSON`. Wartości notowań (sekcja `rates`) są podawane w walucie `PLN` - polski złoty.

### Parametry zapytań

- `{currency_code}` - trzyliterowy kod waluty, np. `USD`,`EUR`
- `{date}` - data w formacie `RRRR-MM-DD`
- `{start_date}` - data początku okresu w formacie `RRRR-MM-DD`
- `{end_date}`- data końca okresu w formacie `RRRR-MM-DD`

### Opcjonalne parametry

Parametry podawane na końcu zapytania po znaku `$`

- `interpolated` - interpolated jest ustawione na `1` dla dni, które swoją wartość przybrały jako tę z poprzedzającego dnia posiadającego notowanie. `0` w przeciwnym przypadku. Przykład poprawnego zapisu: `?interpolated=1`

### Adresacja API

#### Notowanie z danego dnia

`http://host:5000/api/v1/rates/{currency_code}/day/{date}?interpolated=[0,1]`

Przykład zwracanych danych:

`http://host:5000/api/v1/rates/eur/day/2011-01-01`

```
{}
```

Standardowo zwracane są notowania z polem `"interpolated": 0`, czyli takie, które nie zostały sztucznie wygenerowane. W takim wypadku jeżeli wybrany zostanie dzień, w którym banki nie prowadziły notowań to zostanie zwrócony pusty słownik. W celu uwzględnienia w zapytaniu notowań wygenerowanych sztucznie należy zastosować opcjonalny argument `interpolated` w ciele zapytania. Poniżej jest przykład jego zastosowania:

`http://host:5000/api/v1/rates/eur/day/2011-01-01?interpolated=1`

```
{
  "code": "EUR",
  "date": "2011-01-01",
  "interpolated": 1,
  "rate": 3.9603
}
```

Te działanie jest właściwe dla wszystkich zapytań dotyczących notowań walut.

#### Notowania z danego okresu

`http://host:5000/api/v1/rates/{currency_code}/range/{start_date}/{end_date}?interpolated=[0,1]`

Przykład zwracanych danych:

`http://host:5000/api/v1/rates/usd/range/2010-01-01/2010-01-06`

```
[
  {
    "code": "USD",
    "date": "2010-01-04",
    "interpolated": 0,
    "rate": 2.8465
  },
  {
    "code": "USD",
    "date": "2010-01-05",
    "interpolated": 0,
    "rate": 2.8264
  },
  {
    "code": "USD",
    "date": "2010-01-06",
    "interpolated": 0,
    "rate": 2.8493
  }
]
```

`http://host:5000/api/v1/rates/usd/range/2010-01-01/2010-01-04?interpolated=1`

```
[
  {
    "code": "USD",
    "date": "2010-01-01",
    "interpolated": 1,
    "rate": 2.8503
  },
  {
    "code": "USD",
    "date": "2010-01-02",
    "interpolated": 1,
    "rate": 2.8503
  },
  {
    "code": "USD",
    "date": "2010-01-03",
    "interpolated": 1,
    "rate": 2.8503
  },
  {
    "code": "USD",
    "date": "2010-01-04",
    "interpolated": 0,
    "rate": 2.8465
  }
]
```

#### Notowania z całego okresu

`http://host:5000/api/v1/rates/{currency_code}/all?interpolated=[0,1]`

#### Suma sprzedaży z danego dnia

`http://host:5000/api/v1/sales/sum/{date}`

Waluta oryginalna to `USD`, waluta po przeliczeniu to `PLN`.

Przykład zwracanych danych:

`http://host:5000/api/v1/sales/sum/2014-04-28`

```
{
  "date": "2014-04-28",
  "exchange_rate": 3.0368,
  "exchanged_value": 7830.32,
  "original_value": 2578.48
}
```

### Wyjątki

Podczas korzystania z API mogą wystąpić wyjątki spowodowane podaniem nieprawidłowych parametrów lub niepoprawnego działania serwera. Rezultatem jest odpowiedź w formacie `JSON` z dwoma polami `error` i `message`.

Przykładowa wiadomość o wystąpieniu wyjątku:

```
{
  "error": "CurrencyCodeError",
  "message": "Invalid currency code. Valid code should consist of 3 letters"
}
```

**Zdefiniowane wyjątki**
| Nazwa `error` | Wiadomość `message` | Kod HTML |
| ------------- | :------------------:| -------: |
|DateFormatError | Invalid date argument. Date has to be passed in given format: YYYY-MM-DD| 422 |
|RangeOrderError| Dates are in wrong order. End date must be after/equal start date.| 422 |
|OutOfRangeError | Requested range exceedes the maximum range available in database.| 422 |
|CurrencyCodeError | Invalid currency code. Valid code should consist of 3 letters| 422 |
|NoCurrencyError | Requested currency is not available in database.| 422 |
|InterpolatedParamError| Invalid argument value - interpolated should be set as 0 or 1| 422 |
|NoSalesError | There were no sales on given day| 422 |
|InternalServerError | 500 Internal Server Error| 500 |
|DatabaseError | Database connection failed. Please contact server administrator.| 500 |

## Inne

W dostarczonej bazie danych dane o notowań walut zawierają się w zakresie `2010-01-01` - `2020-12-19`.

Dane o sprzedaży zawarte są w zakresie `2014-01-03` - `2017-12-30`.

Dostępne waluty: `USD`, `THB`, `AUD`, `HKD`, `CAD`, `NZD`, `EUR`, `JPY`, `GBP`, `CHF`.

### Struktura bazy danych

Struktura wykorzystywanej bazy danych w pliku `database.sqlite`.

- **Currencies**(<ins>code</ins>)
- **Customers**(<ins>id</ins>, name)
- **Orders**(<ins>row_id</ins>, order_id, order_date, #customer_id, #product_id, value)
- **Products**(<ins>id</ins>, name)
- **Rates**(<ins>#code, date</ins>, rate, interpolated)
