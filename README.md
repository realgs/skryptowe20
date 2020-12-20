# Exchange Rates and Real Estate API
Main goal of this project is to create a very reliable and precise API for PLN exchange rates and real estate data from state of Connecticut. 
Every user with connection to this API is able to request rates from given period and also data about sales in USD and any other actually available currency. 

## First API set-up (installation)
1. Clone this repo to your hard drive.
2. Go to [this link](https://data.world/state-of-connecticut/5mzw-sjtu) and download the .csv file. Save it in the same location as the repo.
3. Open windows console and navigate to cloned directory and run start.bat. This script will automatically create a new python virtual environment* and database. It will also activate this new venv, set-up a database and run the server.

\*Python 3.6 at least must be installed on your computer. 

## Everyday API set-up
1. Open windows console and navigate to directory with cloned files.
2. Run start.bat. This time the script will not generate new venv, but it will activate already existing one and update the database. After that, the server will be started.

## Packages dependencies
This project requires some additional python libraries, but you do not have to worry about installing them. All necessary work is done by start.bat script.

List of packages, just FYI: flask, flask-caching, flask-limiter, requests, pandas.

## How to use API - PLN Exchange Rates
Actually available currencies': USD, EUR, HUF, CHF, GBP, JPY, CZK, AED, BOB, KWD. 
These are also codes that you are supposed to put in {code}.  Arguments marked as {single_date} / {from_date} / {till_date} must be formatted as: YYYY-MM-DD. 
Data is taken from [NBP Api](http://api.nbp.pl), so you can request data from 2002-01-02 till today.

Exchange rates from a single day:
```/rates/inter/{code}/{single_date}```

Exchange rates from last X days:
```/rates/inter/{code}/{last_days}```

Exchange rates from given date till today:
```/rates/inter/{code}/{from_date}/today```

Exchange rates from given period:
```/rates/inter/{code}/{from_date}/{till_date}```

You can also request data without "Interpolated flag". Just remove ```/inter``` from lines presented above.

## How to use API - Sales Data
Available values for {code} are almost the same as for exchange rates. The original currency used in the dataset is USD, so you cannot request for it, but you can request for data calculated to PLN instead.
The data comes from Connecicut real estate dataset. Even though the file's names says: 2001-2017, the actual data is available only for period from 2006-10-01 to 2017-09-29. That's because some parts of original .csv file are spoiled.

Sales data from single day:
```/sales/{code}/{single_date}```

Sales data from given period:
```/sales/{code}/{from_date}/{till_date}```

## Examples of API uses

* Exchange rates of EUR, with "Interpolated flag" from single day: ``/rates/inter/EUR/2020-12-12`` 
	```
	[
	  {
	    "date": "2020-12-12", 
	    "interpolated": 1, 
	    "rate": 4.4385
	  }
	] 
	```
* Exchange rates of USD from last 2 days: ``/rates/USD/2``  OR ``/rates/USD/2020-12-19/today``
	```
	[
	  {
	    "date": "2020-12-19", 
	    "rate": 3.6322
	  }, 
	  {
	    "date": "2020-12-20", 
	    "rate": 3.6322
	  }
	]
	```

* Exchange rates CZK for years 2005 - 2010:  ``/rates/CZK/2005-01-01/2010-12-31`` 

	```
	[
	  {
	    "date": "2005-01-01", 
	    "rate": 0.1341
	  },
	  ...
	  {
	    "date": "2010-12-31", 
	    "rate": 0.158
	  }
	]
	```
* Sales data from single day, calculated to EUR: ``/sales/CZK/2011-01-01/`` 
	```	
	[
	  {
	    "CZK rate": 0.1655, 
	    "CZK sales": 275662159.99, 
	    "Date": "2017-09-29", 
	    "USD rate": 3.6519, 
	    "USD sales": 12492699.0
	  }
	]
	```
* Sales data from whole available period, calculated to PLN:
``/sales/CZK/2006-10-01/2017-09-29`` 
	```
	[
	  {
	    "Date": "2006-10-01", 
	    "PLN sales": 20297564.63, 
	    "USD rate": 3.1425, 
	    "USD sales": 6459050.0
	  },
	  ...
	  {
	    "Date": "2017-09-29", 
	    "PLN sales": 45622087.48, 
	    "USD rate": 3.6519, 
	    "USD sales": 12492699.0
	  }
	]
	```

## Additional info

This API is limited to answer 100 requests per minute and 10000 requests per day from each unique IP address.

Also, by using flask-caching, API is temporary saving requested outputs for 60 seconds by default.