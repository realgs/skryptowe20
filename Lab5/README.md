## PLN to USD rates, sales API

This repository contains files needed to locally run API 
with USD to PLN rates and sales from Superstore sample database taken from 
Learning-Tableau course. It allows to gain exchange rate and sum of sales by day.
for specified date or for range of dates

### Data sources

Database used in comes from Learning-Tableau-10 course.
Originally data is stored in .csv file, which was converted using SQLite3 to database.

https://github.com/PacktPublishing/Learning-Tableau-10/blob/master/Chapter%2001/Superstore.csv


Exchange rates are obtained from http://api.nbp.pl/, supplemented with interpolated 
rates not found in NBP API.

## Get started
### Install packages

In this directory run:
``pip install -r requirements.txt``

### Get data
Download .csv file from:
https://github.com/PacktPublishing/Learning-Tableau-10/blob/master/Chapter%2001/Superstore.csv

And move it to src directory.

Then run database_creation.py:

This will create database with customers, items, sales orders,daily sales data and currency data.

#### Configuration
You can change API configuration in *src/config.py* file. 
You can configure:
- path to database
- requests per user
- cache timeout 

## Usage

Run API by running src/app.py

Go to **http://127.0.0.1:5000**.

With the use of this API you can obtain:
- PLN to USD exchange rate for specified date:
``http://127.0.0.1:5000/rates/usd/{date}``
  - ex. ``http://127.0.0.1:5000/rates/usd/2013-01-01``
- PLN to USD exchange rate for date range:
``http://127.0.0.1:5000/rates/usd/{start_date}/{end_date}``
  - ex. ``http://127.0.0.1:5000/rates/usd/2013-01-01/2014-12-31``
- Sales data for specified date:
``http://127.0.0.1:5000/sales/{date}``
  - ex. ``http://127.0.0.1:5000/sales/2013-01-01``
- Sales data for date range:
``http://127.0.0.1:5000/sales/{start_date}/{end_date}``
  - ex. ``http://127.0.0.1:5000/sales/2013-01-01/2014-12-31``
    
## Defaults

- By default cache timeout is set to 100.
- By default requests limit is set to 10/s per user.

## Project structure

- *src/config.py* - configuration file
- *src/app.py* - main API file, configures API and defines its workflow 
- *src/currency_data.py* - stores functions that obtain and complement data from http://api.nbp.pl/
- *src/database_creation.py* - stores functions that create and populate database with data from Superstore.csv
- *src/database_collector.py* - stores functions for obtaining data from database to be displayed via API.