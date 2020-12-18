# Currency  and Sales API

Currency Sales API is an API, which allows users to request usd exchange rates and sales from years 2003-2005

#Data sources
Database used in this project is a Kaggle sales database from years 2003-2005, which can be found here:
https://www.kaggle.com/kyanyoga/sample-sales-data

## Installation and Dependencies

To run the project properly run the following commands to install proper packages


```bash
pip install requests
pip install flask
pip install flask_limiter
pip install sqlite3
pip install apscheduler
```

This API requires also an existing database. I've included in my repository a database under name the **data.db**.
Database is already filled with sales data from Kaggle and corresponding exchange rates of USD from [NBP API](http://api.nbp.pl/en.html).

## Project structure
The project consists of: **main.py**, serving as a main function, **data.db**, local database with sales and rates. Other file such as **nbp_operations.py**, **db_operations.py**, **validate_operations.py**
are responsible for logic operations of data processing. File **api.py** contains all routes to implemented endpoints, **cache.py** is responsible for all cache operations.
Under **constans.py** you can find all API constans and configure API features such as: 
- default API requests limits
- cache refresh interval
- path to db

```
    .
    ├── api.py
    │── cache.py
    │── constans.py
    ├── db_operations.py
    ├── nbp_operations.py
    │── validate_operations.py
    │
    ├── data.db 
    ├── README.md
    └── main.py  

```

## Usage
To start the API run
```python 
python main.py
```
The API runs under http://127.0.0.1:5000/api address. Available endpoints are listed below. 

## Endpoints
### Get rates for day
  Returns json data about USD to PLN exchange rate for a given day.

**Requests per user**  
- 300 per day, 40 per minute

**URL**

- USD to PLN exchange rate for specified date:
    - ``http://127.0.0.1:5000/rates/{date}``
 - example usage 
    - ``http://127.0.0.1:5000/rates/2005-04-22``

**Success Response:**

  * **Code:** 200   
    **Content:** `{
  "date": "2005-04-22", 
  "interpolated": 0, 
  "usd_rate": 3.2111
}`

### Get rates for data range
  Returns json data about USD to PLN exchange rate for a given period of time.

**Requests per user**  
- 300 per day, 40 per minute

**URL**

- USD to PLN exchange rate for specified period: 
    - ``http://127.0.0.1:5000/rates/{start_date}/{end_date}``
 - example usage 
    - ``http://127.0.0.1:5000/rates/2005-04-22/2005-04-23``

* **Success Response:**

  * **Code:** 200   
    **Content:** `{
  "2005-04-22": {
    "date": "2005-04-22", 
    "interpolated": 0, 
    "usd_rate": 3.2111
  }, "2005-04-23": {
    "date": "2005-04-23", 
    "interpolated": 1, 
    "usd_rate": 3.2111
  }
}`


### Get sales for day
  Returns json data about sales, represented in USD and PLN for a given day.

**Requests per user**  
 - 200 per day, 30 per minute

**URL**

- sales data in USD and PLN for specified date:
    - ``http://127.0.0.1:5000/sales/{date}``
 - example usage 
    - ``http://127.0.0.1:5000/sales/2005-04-22``

**Success Response:**

  * **Code:** 200   
    **Content:** `{
  "date": "2005-04-22", 
  "pln_sale_sum": 187647.1791, 
  "usd_rate": 3.2111, 
  "usd_sale_sum": 58437.04
}`   
    
### Get sales for data range
  Returns json data about sales represented in USD and PLN for a given period of time.

**Requests per user**  
 - 200 per day, 30 per minute

**URL**

-  sales data in USD and PLN for specified period: 
    - ``http://127.0.0.1:5000/sales/{start_date}/{end_date}``
 - example usage 
    - ``http://127.0.0.1:5000/sales/2005-04-14/2004-04-15ą``

* **Success Response:**

  * **Code:** 200   
    **Content:** `{
  "2005-04-14": {
    "date": "2005-04-14", 
    "pln_sale_sum": 114134.3036, 
    "usd_rate": 3.1988, 
    "usd_sale_sum": 35680.35
  }, 
  "2005-04-15": {
    "date": "2005-04-15", 
    "pln_sale_sum": 83672.9976, 
    "usd_rate": 3.2166, 
    "usd_sale_sum": 26012.87
  }}`
  
     
## Error Response Codes


**WRONG_DATE_FORMAT**

  * **Code:** 400  
  * **Content:** `{'message': 'Wrong date format provided, correct format is YYYYY-MM-DD'}`

**WRONG_DATE_RANGE**

  * **Code:** 416  
  * **Content:** `{'message': 'Date out of valid range, valid range is 2003-05-05 to 2005-05-05'}`
    
**WRONG_DATE_ORDER**

  * **Code:** 400  
  * **Content:** `{'message': 'Maximum date range exceeded. Maximum amount of days - 366.'}`

**NO_DATA_FOUND**

  * **Code:** 404  
  * **Content:** `{'message': 'No data found for given date'}`


## Others
- Shared limit of requests for entire application is stored  **constans.py** and set by default to: 
    - APPLICATION_REQUEST_LIMIT:  `3000 per day and 400 per hour`
- By default cache refresh interval is set to `12 hours`
- Request limits for sale and rates are stored in **constans.py** and they are set by default to:
    - REQUEST_LIMIT_RATE `300 per hour, 40 per minute`
    - REQUEST_LIMIT_SALE `200 per hour, 30 per minute`
- By default START_DATE and END_DATE are set to boundary date values in Kaggle datbabase which is:
    * START_DATE: `2003-05-05`
    * END_DATE: `2005-05-05`
- Supported date format is (YYYY-mm-dd)
    * example: `2005-01-02`