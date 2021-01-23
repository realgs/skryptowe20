# Exchange rates and sales API

This repository contains files, that allow to locally run API with USD to PLN exchange rates and daily sales in both USD and PLN from Northwind sample database.

## Data sources

Database is a version of the Microsoft Access 2000 Northwind sample database, re-engineered for SQLite3 - https://github.com/jpwhite3/northwind-SQLite3. This base is extended by tables ExchangeRate and TotalSales

USD to PLN exchange rates come from here - http://api.nbp.pl/

## Installation

To run the project one needs Python 3.6.1 (minimum version supported by pandas)


Then, navigate to project directory from the console and there run the commands: 

```
pip install flask
pip install Flask-Limiter
pip install requests
pip install Flask-Caching
pip install pandas
```

## Usage

From here you will be able to run the app, in the project directory, simply run:

```
api.py
```

Having done that, this API allows you to get following data:

- USD to PLN exchange rate at date:  
``http://127.0.0.1:5000/api/rates/USD/{date}``
  
   - example ``http://127.0.0.1:5000/api/rates/USD/2020-02-20``
   
- USD to PLN exchange rate from the start_date to end_date:             
``http://127.0.0.1:5000/api/rates/USD/{start_date}/{end_date}``
  - example ``http://127.0.0.1:5000/api/rates/USD/2013-04-07/2014-10-22``
  
- sales data at date:  
``http://127.0.0.1:5000/api/sales/{date}``
  - example ``http://127.0.0.1:5000/api/sales/2013-01-01``
  
- sales data from start_date to end_date:         
``http://127.0.0.1:5000/api/sales/{start_date}/{end_date}``
  - example ``http://127.0.0.1:5000/api/sales/2013-04-07/2014-10-22``

Alternatively, instead of **127.0.0.1**, you could use **localhost**, those are the same


## Limits 

- Available dates for the exchange rate part range from **2002-01-02** to today

- Available dates for the sales part range from **2012-07-04** to **2016-02-19**

- **YYYY-MM-DD** is the only acceptable date formatting

- There is a request limit that allows 20 request per minute of every request type

- There is a cache timeout set for 100s


## Project Structure

*api.py* - main program logic, responsible for the API requests

*db_handler.py* - file providing methods to access the data from the database

*database.db* - The expanded database mentioned before

##

