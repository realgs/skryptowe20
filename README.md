# Exchange rates and sales API
## Description

Exchange rates and sales API is a service for historical foreign exchange rates published by the National Bank of Poland (http://api.nbp.pl/) and sales data in **json** format. Sales data come from the database (*‘database.db’*) shared in this repository.
Exchange rate data and sales data are available **from 2014-12-28 to 2016-12-28**.

## Project structure
* `wsgi.py` - startup script
* `my_requirements.txt` - contains a set of required packages
* `frontend/` - Vue.js user interface
* `lab5_solutions/api.py` - script responsible for the functioning of the API
* `lab5_solutions/currency.py` - currencies available in the application
* `lab5_solutions/database.db` - database file containing sales and exchange rates data
* `lab5_solutions/database_repository.py` - script containing functions to connect to and operate on the database
* `lab5_solutions/exceptions.py` - domain exceptions
* `lab5_solutions/nbp_api.py` - script containing the function to manage client for the NBP API
* `lab5_solutions/utils.py` - contains useful variables
* `lab5_solutions/templates/home.html` - HTML document for the start page




## Quick start
### First option
In your browser, run the website:
### https://sale-and-exchange-rate.herokuapp.com/

That's all! Read the Usage section and enjoy the exchange rates and sales data. 
### Second option
You will need **Python 3.7.x (or higher)**. 

To get Python 3, follow this link:
https://www.python.org/downloads/, 
select the Python 3.7.x version and install.
To check if Python is installed correctly, open a command line and run  these commands:

`python --version`

`pip --version`

The outputs of these commands should contain information about Python 3.7.x.

I can highly recommend Python 3.7.9., because this version was used in development and testing the project.

*my_requirements.txt* - contains the set of packages that this application depends on. To install them, use this command in terminal/command line:

`pip install -r my_requirements.txt`


To start, use this command:

`python wsgi.py`

Now head over to **http://127.0.0.1:5000/** (or **http://localhost:5000/**), and you should see the home page.

## Usage
### Currency
Currently available currencies are: 
* USD (U.S. Dollar),
* EUR (Euro)
* GBP (British pound sterling).

Currency codes are based on the ISO 4217 standard.

### Date format
The expected date format is **YYYY-MM-DD** (ISO 8601 standard), e.g. 2015-10-13.

### Endpoints
There are currently four endpoints you can use.

#### Get the exchange rate of the selected currency on the selected day
`/exchange-rates/{currency}/{date}`

Example:

`/exchange-rates/GBP/2015-10-13`

Result:

```json
{
  "rates": [
    {
      "currency": "GBP", 
      "date": "2015-10-13", 
      "interpolated": false, 
      "rate": 5.6705
    }
  ]
}
```

#### Get the exchange rates of the selected currency in the selected time period

`/exchange-rates/{currency}/{start_date}/{end_date}`

Example:

` /exchange-rates/EUR/2015-12-11/2015-12-14`

Result:

```json
{
  "rates": [
    {
      "currency": "EUR", 
      "date": "2015-12-11", 
      "interpolated": false, 
      "rate": 4.3471
    }, 
    {
      "currency": "EUR", 
      "date": "2015-12-12", 
      "interpolated": true, 
      "rate": 4.3471
    }, 
    {
      "currency": "EUR", 
      "date": "2015-12-13", 
      "interpolated": true, 
      "rate": 4.3471
    }, 
    {
      "currency": "EUR", 
      "date": "2015-12-14", 
      "interpolated": false, 
      "rate": 4.35
    }
  ]
}
```

#### Get sales data for the selected date

`/sales/{date}`

Example:

`/sales/2016-10-13`

Result:

```json
{
  "sales": [
    {
      "date": "2016-10-13", 
      "pln": 2487.38, 
      "usd": 522.0
    }
  ]
}
```

Example:

`/sales/2015-02-12`

Result:

```json
{
  "sales": [
    {
      "date": "2015-02-12", 
      "pln": 0, 
      "usd": 0
    }
  ]
}
```

#### Get sales data  in the selected time period

`/sales/{start_date}/{end_date}`

Example:

`/sales/2016-10-13/2016-10-15`

Result:

```json
{
  "sales": [
    {
      "date": "2016-10-13", 
      "pln": 2487.38, 
      "usd": 522.0
    }, 
    {
      "date": "2016-10-14", 
      "pln": 2699.09, 
      "usd": 567.0
    }, 
    {
      "date": "2016-10-15", 
      "pln": 1042.51, 
      "usd": 219.0
    }
  ]
}
```
### Exchange rate response

```
{
  "rates": [
    {
      "currency": {currency}, 
      "date": {date}, 
      "interpolated": {true | false}, 
      "rate": {rate}
    }
  ]
}
```
* *currency* - currency code in the ISO 4217 standard
* *date* - date of the currency exchange rate in the ISO 8601 standard
* property *interpolated* is set to **true** for days that had no value and took their value from the previous (or next, depending on the situation) day that had the exchange rate. **False** otherwise.
* *rate* - selected currency to PLN exchange rate

### Sales data response
```
{
  "sales": [
    {
      "date": {date}, 
      "pln": {PLN}, 
      "usd": {USD}
    }
  ]
}
```
* *date* - date of the sale in the ISO 8601 standard
* *pln* - sum of the total sales on the selected day in PLN counted using the exchange rate for the day. In case of no sale on that date it is equal to 0.
* *usd* - sum of the total sales on the selected day in the original currency (USD). In case of no sale on that date it is equal to 0.

### Types of bad requests
Making a request with any of the following types of errors results in the **HTTP 400 Bad request** response status code.
* Using an unsupported currency in the request
* Using a date from an unsupported time period
* Using an end date that is before a start date
* Using invalid date format

## Limits
Requests limit is set to **500 per day** and **30 per hour**, 
both per user. After exceeding the limit, the client will receive the **HTTP 429 Too Many Requests** response status code.

## Cache
Project provides an application caching mechanism. Application stores exchange rates and sales data to reference later.
Cache timeout is set to **24 hours**.