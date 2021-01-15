# Currency exchange and sales api

## How to start

### 1.Api is available at the URL: https://currencyandsales.herokuapp.com

### 2.Local host
- Install required packages:
```Bash
pip install -r requirements.txt
```
- Run app:
```Bash
python Api.py
```
## Some explanations and rules
{code} - three letter currency code <br>
{date},{startDate},{endDate} - date in format: "yyyy-mm-dd"<br><br>

There are per-person query limits:<br>
1 per second<br>
50 per hour<br>
200 per day<br>

## Routes
### /rates/{code}/{date}
Returns the exchange rate for the {Code} currency on {date}<br>
Returns 400_BAD_REQUEST when {date} format is incorrect<br>
Returns 404_NOT_FOUND when there is no exchange rate with code={code} and date={date} in the database<br>

### /rates/{code}/{startDate}/{endDate}
Returns the exchange rates for the {Code} currency between {startDate} and {endDate}<br>
Returns 400_BAD_REQUEST when {startDate} or {endDate} format is incorrect or when {startDate} is after {endDate}<br>
Returns 404_NOT_FOUND when there is no exchange rate with code={code} and date between {startDate} and {endDate}<br><br>

Results are cached for 10 minutes<br>

### /sales/{date}
Returns the sales result on {date}<br>
Returns 400_BAD_REQUEST when {date} format is incorrect<br>
Returns 404_NOT_FOUND when there is no sale result with date={date} in the database<br>

### /sales/{startDate}/{endDate}
Returns the sales results between {startDate} and {endDate}
Returns 400_BAD_REQUEST when {startDate} or {endDate} format is incorrect or when {startDate} is after {endDate}<br>
Returns 404_NOT_FOUND when there is no sale result with date between {startDate} and {endDate}<br><br>

Results are cached for 10 minutes<br>

## Examples
### /rates/TTD/2015-02-03
```json
{
    "_id": {
        "$oid": "5fdf150020e745a2f741a4b5"
    },
    "code": "TTD",
    "date": {
        "$date": 1422921600000
    },
    "dateStr": "2015-02-03",
    "interpolated": true,
    "mid": 0.5891
}
```

### /rates/EUR/2020-02-03/2020-02-05
```json
[
    {
        "_id": {
            "$oid": "5fdf140220e745a2f73c2a5a"
        },
        "code": "EUR",
        "date": {
            "$date": 1580688000000
        },
        "dateStr": "2020-02-03",
        "interpolated": false,
        "mid": 4.3034
    },
    {
        "_id": {
            "$oid": "5fdf140220e745a2f73c2a5b"
        },
        "code": "EUR",
        "date": {
            "$date": 1580774400000
        },
        "dateStr": "2020-02-04",
        "interpolated": false,
        "mid": 4.2867
    },
    {
        "_id": {
            "$oid": "5fdf140220e745a2f73c2a5c"
        },
        "code": "EUR",
        "date": {
            "$date": 1580860800000
        },
        "dateStr": "2020-02-05",
        "interpolated": false,
        "mid": 4.262
    }
]

```
code - three letter currency code <br>
date - date as DateField<br>
dateStr - date as string<br>
interpolated - true when exchange rate is copied from last rate in NBP data, false otherwise<br>
mid - value of exchange rate ({code} -> PLN)<br>

### /sales/2017-05-23
```json
{
    "_id": {
        "$oid": "5fdf161d20e745a2f749924f"
    },
    "date": {
        "$date": 1495497600000
    },
    "dateStr": "2017-05-23",
    "pln": 17200.76992,
    "usd": 4604.8
}
```

### /sales/2018-04-22/2018-04-24
```json
[
    {
        "_id": {
            "$oid": "5fdf161d20e745a2f749933d"
        },
        "date": {
            "$date": 1524355200000
        },
        "dateStr": "2018-04-22",
        "pln": 8770.943875,
        "usd": 2588.75
    },
    {
        "_id": {
            "$oid": "5fdf161d20e745a2f749933e"
        },
        "date": {
            "$date": 1524441600000
        },
        "dateStr": "2018-04-23",
        "pln": 11568.29564,
        "usd": 3386.9
    },
    {
        "_id": {
            "$oid": "5fdf161d20e745a2f749933f"
        },
        "date": {
            "$date": 1524528000000
        },
        "dateStr": "2018-04-24",
        "pln": 5560.8356475,
        "usd": 1616.475
    }
]
```
date - date as DateField<br>
dateStr - date as string<br>
pln - value of sale result in PLN<br>
usd - value of sale result in USD<br>

### 400_BAD_REQUEST
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Bad request</title>
<h1>Bad request</h1>
<p>Invalid request</p>
```
### 404_NOT_FOUND
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Not found</title>
<h1>Not found</h1>
<p>404: No data found in date range: <2012-04-23, 2012-04-24></p>
```

### 429_TOO_MANY_REQUESTS
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>429 Too Many Requests</title>
<h1>Too Many Requests</h1>
<p>1 per 1 second</p>
```
