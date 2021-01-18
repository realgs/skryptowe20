# Currencies rates and sales REST API

## Installation

Clone this repository, then run the following commands inside the `src` folder:
```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Database comes from this repository:

`github.com/jpwhite3/northwind-SQLite3`

Simply unzip the database and put it into `src` folder and call it `sales.sqlite`.

## Running the server

When you start server for the first time, make sure to use `-i` or `--init` flag:
```bash
venv\Scripts\Activate.ps1
python server.py -i
```
It creates required tables and fills them with values from NBP API.

## Usage

### API for currencies rates
Today's rates:
```
currency/{currency}/time/today
```
Rates from given day:
```
currency/{currency}/time/{day}
```
List of rates from period of time:
```
currency/{currency}/time/{from}/{to}
```
List of rates from last few days:
```
currency/{currency}/last/{days}
```

### API for sales

Sum of sales from given day:
```
sales/{currency}/time/{day}
```
List of sales from each day in given period of time:
```
sales/{currency}/time/{from}/{to}
```

## Returned data

API returns list of objects on success or error message if something goes wrong. Here is an example JSON returned by currencies rates API:
```json
[
    {
        "date": "2020-12-18",
        "interpolated": false,
        "exchange_rate": 4.4493
    }
]
```
...and JSON from sales API:
```json
[
    {
        "desired": 1211.43,
        "original": 1638.4,
        "date": "2013-10-10"
    }
]
```
## Examples
```
currency/usd/time/today
```

```
currency/eur/time/today
```

```
currency/usd/time/2020-10-10
```

```
currency/usd/time/2010-01-05
```

```
currency/usd/time/2010-01-05/2020-10-10
```

```
currency/eur/last/10
```

```
sales/eur/time/2013-08-30
```

```
sales/usd/time/2012-11-11/2013-03-23
```
