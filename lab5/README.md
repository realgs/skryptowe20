# Lab 5 My first API
This is an API for getting historical currency ratings from 
NBP API completed with data for missing ratings. You can also 
access total sales data from provided database using this api.
#Quickstart
1. Install Python 3.7 or up on your computer: https://www.python.org/downloads/
2. Go to the downloaded project directory by running `cd <repo_address>`
3. `python -m pip install flask`
4. `python -m pip install Flask-Limiter`
5. Run `python api.py` to start the API
#User manual
API requests return data in JSON format. Data is available for dates between 
2013-01-04 and 2016-12-29.
<br/>
Supported currencies:
- USD
- PLN 

API uses rate limiting: 300 request per day, 20 requests per minute. After 
the limit has been surpassed new request will result in 429 Too Many Requests
error.

Request parameters:
- {code} - three-letter currency code (ISO 4217 standard)
- {date}, {startDate}, {endDate} - date in YYYY-MM-DD format (ISO 8601 standard)

Possible requests:
- `/api/rates/{code}/{date}` returns specified currency rate from given day 
with 'Interpolated' parameter. That parameter is true if the currency rate 
was not available on NBP API and has been substituted with currency rate 
from previous day. Otherwise it is false.
- `/api/rates/{code}/{startDate}/{endDate}` 
- `/api/sales/{date}`
- `/api/sales{startDate}/{endDate}`
