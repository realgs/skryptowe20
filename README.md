# Sales API

Sales API is an API, which allows users to request usd exchange rates and sales data from [sales data sample](https://www.kaggle.com/kyanyoga/sample-sales-data) found on Kaggle.
The data is from years 2004 and 2005.

## Installation

Packages required to properly run the project are listed in **requirements.txt** file. To install them run:

```bash
pip install -r requirements.txt
```
or (for Python3 users):
```bash
pip3 install -r requirements.txt
```

The API also requires sales and exchange rates data. The database should exist in the main project directory (directory with app.py) under the name **data.db**. I included an empty database in the repository. To populate it with sales data simply connect with sqlite3 and follow the instructions found [here](https://www.sqlitetutorial.net/sqlite-import-csv/#:~:text=First%2C%20from%20the%20menu%20choose,shown%20in%20the%20picture%20below.). The API will get exchange rates data from [NBP API](http://api.nbp.pl/en.html).

## Project structure
The project consists of: **app.py**, serving as a main function, **data.db** (both of those located in the main project directory) and **/api** directory, containing all of the logic. Under **api/** you will find **routes/** directory, containg routes all endpoints, configuration and database management files, date validators and **nbp_data.py** file, responsible for requesting and properly transforming exchange rates data.
```
    .
    ├── api 
    │   ├── routes
    │   │   ├── rates.py
    │   │   ├── sales.py
    │   ├── __init__.py
    │   ├── config.py
    │   ├── manage_db.py
    │   ├── nbp_data.py
    │   └── validators.py
    │
    ├── data.db 
    ├── README.md
    └── app.py  

```

## Usage
To start the API run (when in main project folder):
```python
python app.py
```
The API runs under http://127.0.0.1:5000/api address. Available endpoints are listed below. 
* **Global request limit**  
1000 per day, 400 per hour
## Endpoints
**Get rates for day**
----
  Returns json data about an exchange rate for a given day.
* **Requests per user**  
200 per day, 30 per minute

* **URL**

  /api/rates/:date `GET`

  
*  **URL Params**
 
   `date=[string] (YYYY-mm-dd) format`


* **Success Response:**

  * **Code:** 200   
    **Content:** `{"date": "2004-07-03", "interpolated": 1, "rate": 3.7166}`
 
* **Error Response:**

  * **Code:** 400  
    **Content:** `{'message': 'Incorrect date format.'}`

  OR

  * **Code:** 404  
    **Content:** `{'message': 'No data found for given date.'}`
    
**Get rates for period**
----
  Returns json data about exchange rates for a given period. Maximum date span is 366 days.
* **Requests per user**  
200 per day, 30 per minute

* **URL**

  /api/rates/:start_date/:end_date `GET`

  
*  **URL Params**
 
   `start_date=[string] (YYYY-mm-dd) format`
   `end_date=[string] (YYYY-mm-dd) format`


* **Success Response:**

  * **Code:** 200   
    **Content:** `{"rates": [ {"date": "2004-07-03", "interpolated": 1, "rate": 3.7166}, {"date": "2004-07-04", "interpolated": 1, "rate": 3.7166}]}`
 
* **Error Response:**

  * **Code:** 400  
    **Content:** `{'message': 'Incorrect date format.'}`

  OR

  * **Code:** 400  
    **Content:** `{'message': 'Maximum date range exceeded. Maximum amount of days - 366.'}`

  OR

  * **Code:** 404  
    **Content:** `{'message': 'No data found for given date.'}`

**Get last n rates**
----
  Returns json data about last n rates.
* **Requests per user**  
200 per day, 30 per minute

* **URL**

  /api/rates/last/:days `GET`

  
*  **URL Params**
 
   `days=[integer]`

* **Success Response:**

  * **Code:** 200   
    **Content:** `{"rates": [{"date": "2005-12-31",  "interpolated": 1, "rate": 3.2613}, {"date": "2005-12-30", "interpolated": 0, "rate": 3.2613}]}`
 
* **Error Response:**

  * **Code:** 400  
    **Content:** `{'message': 'Incorrect days amount. Maximum amount is 100.'}`

**Get sales for day**
----
  Returns json data about sales (in two currencies) for a given day.
* **Requests per user**  
200 per day, 30 per minute

* **URL**

  /api/sales/:date `GET`

  
*  **URL Params**
 
   `date=[string] (YYYY-mm-dd) format`


* **Success Response:**

  * **Code:** 200   
    **Content:** `{"date": "2004-07-19", "pln": {"sale": 146869.1487}, "usd": {"sale": 41297.14}}`
 
* **Error Response:**

  * **Code:** 400  
    **Content:** `{'message': 'Incorrect date format.'}`

  OR

  * **Code:** 404  
    **Content:** `{'message': 'No data found for given date.'}`
    
**Get sales for period**
----
  Returns json data about sales (in two currencies) for a given period. Maximum date span is 366 days.
* **Requests per user**  
200 per day, 30 per minute

* **URL**

  /api/sales/:start_date/:end_date `GET`

  
*  **URL Params**
 
   `start_date=[string] (YYYY-mm-dd) format`
   `end_date=[string] (YYYY-mm-dd) format`


* **Success Response:**

  * **Code:** 200   
    **Content:** `{"sales": [{"date": "2004-07-19", "pln": {"sale": 146869.1487}, "usd": {"sale": 41297.14}}, {"date": "2004-07-20", "pln": {"sale": 245126.451}, "usd": {"sale": 68270.84}}]}`
 
* **Error Response:**

  * **Code:** 400  
    **Content:** `{'message': 'Incorrect date format.'}`

  OR

  * **Code:** 400  
    **Content:** `{'message': 'Maximum date range exceeded. Maximum amount of days - 366.'}`

  OR

  * **Code:** 404  
    **Content:** `{'message': 'No data found for given date.'}`
