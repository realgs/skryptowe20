# BikeSales API

## Installation

This project was developed and tested using Python 3.9.1, although no new  language features were used, so it should work for any version starting from Python 3.6.1 (minimum version supported by pandas)

No environment variables setup is required, as the server is configurable via command line arguments.

The required dependencies are listed in the [`requirements.txt`](requirements.txt) file. To install them, use the command:

```bash
pip install -r requirements.txt
```

To run the server, an SQL Server sample database 'BikeStores' is required. Additionaly, it has to be converted to sqlite in order to be used by the server. If you're running the server for the first time, use the **--update** parameter to create all the necessary tables inside the existing database and fill them with data ([NBP web API will be used](http://api.nbp.pl/)). The repository contains a full database, which was last updated on 2020-12-16.

## Usage

To start the server, use the [`run.py`](run.py) script with optional parameters:

```text
usage: run.py [-h] [-p PORT] [-u] [-d]

Server that provides an API for accessing PLN to USD daily exchange rates and daily bike store sales in both PLN and USD currencies.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Choose the port on which the server will run. (default: 8080)
  -u, --update          Update all rates and sales in the database before starting the server by using the NBP API. (default: False)
  -d, --debug           Run Flask in debug mode. (default: False)
```

By default the server runs on ```localhost:8080```.

Date format used in both requests and responses is **YYYY-MM-DD**.
Requests with date format of **YYYY-M-D** are also accepted.

Currently, there are three endpoints you can use:

### /rates/\<date_start>/\<date_end>

Provides PLN to USD exchange rate for the time period between `date_start` and `date_end` (inclusive)

The responses will be cached for 5 minutes.

The server can respond with:

* A dictionary with one key `rates`, containing an ordered list of dictionaries for every day of the time period specified in the request. The dictionary for a single day contains three keys:

  * `date`: *string of format YYYY-MM-DD* - date on which the exchange rate was determined
  * `rate`: *double* - exchange rate from PLN to USD
  * `interpolated`: *boolean* - whether the exchange rate was interpolated based on previous values

* Bad request if the date format is invalid

* Bad request if the `date_start` is earlier than `date_end`

* Bad request if the time period is longer than 366 days

* Too many requests if the user made more requests than:

  * 1 per second
  * 10 per minute
  * 100 per hour

* Message stating that the data was not found if the time period starts before 2002-01-02 or ends after the day that the database was last updated.

### /rates/\<date>

Redirects to `/rates/<date>/<date>`

### /sales/\<date>

Provides the total sales value for a given day.

The responses will be cached for 10 minutes.

The server can respond with:

* A dictionary with one key `sales`, containing another dictionary with three keys:

  * `date`: *string of format YYYY-MM-DD* - date on which the sales were recorded
  * `original_sales`: *double* - value of total sales made on a given day in USD
  * `exchanged_sales`: *double* - value of total sales made on a given day, converted to PLN using the exchange rate from /rates route for a given day

* Bad request if the date format is invalid

* Too many requests if the user made more requests than:

  * 1 per second
  * 10 per minute

* Message stating that the data was not found if the time period starts before 2016-01-01 or ends after 2018-12-28.

## Examples

### /rates/2020-12-16

```json
{
    "rates": [
        {
            "date": "2020-12-16",
            "interpolated": false,
            "rate": 3.6334
        }
    ]
}
```

### /rates/2019-12-30/2020-01-01

```json
{
    "rates": [
        {
            "date": "2019-12-30",
            "interpolated": false,
            "rate": 3.8027
        },
        {
            "date": "2019-12-31",
            "interpolated": false,
            "rate": 3.7977
        },
        {
            "date": "2020-01-01",
            "interpolated": true,
            "rate": 3.7977
        }
    ]
}
```

### /rates/2020.12.16

```json
{
    "message": "Invalid date format"
}
```

### /rates/2020-12-17/2020-11-17

```json
{
    "message": "date_start cannot be earlier than date_end"
}
```

### /sales/2018-12-28

```json
{
    "sales": {
        "date": "2018-12-28",
        "exchanged_total": 24471.22,
        "original_total": 6516.97
    }
}
```

### /sales/2018-12-27

```json
{
    "sales": {
        "date": "2018-12-27",
        "exchanged_total": 0,
        "original_total": 0
    }
}
```

### /sales/2018-12-29

```json
{
    "message": "No data for this date."
}
```
