# Currency and sales API

This repository consists of files needed to run (locally) API with USD and PLN exchange rates and sales from Northwind sample database.

## Data sources

Database used in this project is a Northwind samlpe database, re-engineered for SQLite3, which is available here: https://github.com/jpwhite3/northwind-SQLite3

USD exchange rates are obtained from http://api.nbp.pl/, complemented with values for days without ratings and saved to database.

## Prerequisites
### Install packages

In this project directory run:

``pip install -r requirements.txt``

### Get database
To use this API you need to download database. Run:

``git clone https://github.com/jpwhite3/northwind-SQLite3.git``

Unzip Northwind_large.sqlite.zip and put Northwind_large.sqlite to this project directory.
Then run:

``python src/populate_db_ref_data.py``

This will populate your database with currency and sales data used by API.

### Configure API

You can change API configuration in *src/conf.py* file. 
You can configure:
- path to database
- default API requests limit per user 
- default cache timeout 

## Usage

Run API with:

``python src/api.py``

Visit **http://127.0.0.1:5000** and follow instructions on the screen.

With the use of this API you can obtain following data:
- USD to PLN exchange rate for specified date:
``http://127.0.0.1:5000/rates/usd/{date}``
  - example usage ``http://127.0.0.1:5000/rates/usd/2013-01-01``
- USD to PLN exchange rate for specified date:
``http://127.0.0.1:5000/rates/usd/{start_date}/{end_date}``
  - example usage ``http://127.0.0.1:5000/rates/usd/2013-01-01/2014-12-31``
- sales data for specified date:
``http://127.0.0.1:5000/sales/{date}``
  - example usage ``http://127.0.0.1:5000/sales/2013-01-01``
- USD to PLN exchange rate for specified date:
``http://127.0.0.1:5000/sales/{start_date}/{end_date}``
  - example usage ``http://127.0.0.1:5000/sales/2013-01-01/2014-12-31``
    
## Others

- By default cache timeou is set to 100.
- By default requests limit is set to 10/s per user.

## Project structure

- *src/conf.py* - configuration file
- *src/api.py* - main API file, configures API and defines its workflow 
- *src/ccy_data.py* - stores functions that obtain and complement data from http://api.nbp.pl/
- *src/sales_data.py* - stores functions that calculate sales in database
- *src/populate_db_ref_data.py* - populates database with additional tables (with USD prices and sales data)
- *src/utils.py* - stores variables and methods used throughout whole project