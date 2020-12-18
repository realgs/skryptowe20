# Sales API
## Introduction
This API allows users users to query PLN exchange rates on specific days and periods.
In addition it allows to obtain information about sales on given days and periods, stored in database. Response contains
sale in USD and PLN, converted at the daily rate.
## Table of contents
1. [Requirements & launch](#requirements-and-launch)
2. [Usage](#usage)
3. [Limits](#limits)
3. [Errors](#errors)
4. [Cache](#cache)
5. [Dependencies](#dependencies)
6. [Sources](#sources)

### Requirements and launch
First of all, simply clone this repository
```
git clone https://github.com/rasiaq/skryptowe20.git
```
and switch to lab5 branch
```
git checkout lab5
```
To run this API on your local machine you will need to install those python packages:
```
pip install Flask
pip install Flask-Limiter
pip install schedule
```
and if you want to use nbp_api_handler, you will also need
```
pip install requests
```
Link to each one of them is listed in [dependencies](#dependencies) section.  
Pre-filled database with values from [sample sales data](https://www.kaggle.com/kyanyoga/sample-sales-data) and USD 
exchange rates from years 2003-2004 is included in the repository. Please make sure that location of database file,
given in ```constans.py``` matches the one on your local machine.
If everything is correct just simply run api_manager.py
```
python3 api_manager.py
```
or start it from your IDE if you are using one.

### Usage
Base API address is `http://127.0.0.1:5000/` and you should see it in a console, right after a start. Endpoints are 
listed below
* GET `/api/rates/<date>`  
    - Description: Returns dict containing currency code and rate for specified date. Interpolated value means whether rate was given
      by [NBP API](http://api.nbp.pl) or taken from previous/next day.  
    - Usage: `http://127.0.0.1:5000/api/rates/2003-01-01`  
    - Result: 
```json
{
  "currency": "usd",
  "rates": [
    {
      "date": "2003-01-01",
      "rate": 3.8388,
      "interpolated": 1
    }
  ]
}
```

* GET `/api/rates/<start_date>/<end_date>`
    - Description: Returns dict containing currency code and table of rates for specified period.  
    - Usage: `http://127.0.0.1:5000/api/rates/2003-01-01/2003-01-02` 
    - Result:
```json
{
  "currency": "usd",
  "rates": [
    {
      "date": "2003-01-01",
      "rate": 3.8388,
      "interpolated": 1
    },
    {
      "date": "2003-01-02",
      "rate": 3.8283,
      "interpolated": 0
    }
  ]
}
```

* GET `/api/sales/2003-01-06`
    - Description: Returns dict containing sale for specified date in USD and PLN
    - Usage: `http://127.0.0.1:5000/api/sales/2003-01-06`
    - Result
```json
{
  "sale": [
    {
      "date": "2003-01-06",
      "rate": 3.8204,
      "usd_sale": 12133.25,
      "pln_sale": 46353.868299999995
    }
  ]
}
```

* GET `/api/sales/<start_date>/<end_date`
    - Description: Returns dict containing sale for specified period in USD and PLN 
    - Usage `http://127.0.0.1:5000/api/sales/2003-01-01/2003-01-09`
    - Result:
```json
{
  "sale": [
    {
      "date": "2003-01-06",
      "rate": 3.8204,
      "usd_sale": 12133.25,
      "pln_sale": 46353.868299999995
    },
    {
      "date": "2003-01-09",
      "rate": 3.828,
      "usd_sale": 11432.34,
      "pln_sale": 43762.99752
    }
  ]
}
```
### Limits
Limits for requests per user are listed in table below  
| Hour | Day |
| --- | --- |
| 200 per hour | 1000 per day |  

These are fully configurable in `constants.py`
``` python
DEFAULT_DAY_LIMIT = '1000 per day'
DEFAULT_HOUR_LIMIT = '200 per hour'
```

### Errors
There are some pre-defined responses which are returned when error occurs  
* Invalid date format
    - Code: 400
    - Message: `"{error": "Invalid date format"}`

* No data for specified date
    - Code: 404
    - Message `{"error": "There is no data for given year"}`

* Specified dates are out of data range
    - Code: 416
    - Message `{"error": "Dates out of available range"}`
    
* Given dates are in a wrong order
    - Code: 400
    - Message: `{"error": "Wrong dates order"}`

### Cache
There is a cache mechanism implemented in `cache.py`. When you start an API, daemon thread schedules and takes care of  
cache updates in the background.  
By default, at the start it writes all data from database (rates and sales for 2003-01-01 - 2004-12.31) into a cache, 
so when there request is made, api manager takes data from it instead of making query to database. 
Cache is reloaded every day at 12:00.  
You can disable that option, by setting
```
DEFAULT_CACHING = True
```
in `constants.py `to False. From that point, cache is updated after every request. To be more specific - program starts with an empty cache
and when the request is made api manager checks if requested data is already in there - if not it takes needed values 
from database and writes then into a cache. Cache daemon is clearing cache everyday at 12:00

### Dependencies
* [Flask](https://palletsprojects.com/p/flask/)
* [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)
* [Schedule](https://github.com/dbader/schedule)
* [Requests](https://requests.readthedocs.io/en/master/)

### Sources
* [NBP API](http://api.nbp.pl)
* [Kaggle sample sales data](https://www.kaggle.com/kyanyoga/sample-sales-data)