# Rates and sales API
An application that allows you to download currency rates and the total daily sales from the store database using the API

### Data sources
Used database supplemented with needed tables:

https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2019.bak

Exchange rates are obtained from http://api.nbp.pl/, supplemented with interpolated 
rates not found in NBP API.

## Get started
### Install packages

In this directory run:
``pip install -r requirements.txt``

## Usage

### Useful information

By default, the application starts at: http://127.0.0.1:5000/
Date format: YYYY-MM-DD (e.g. 2013-07-23)
Currency format: XXX (e.g. PLN)

### Available API functionalities
- Request for currency rates:
``http://127.0.0.1:5000/rates/currency/date_from/date_to``
- Request for currency sales:
``http://127.0.0.1:5000/sales/currency/date``
