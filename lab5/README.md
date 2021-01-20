# Lab 5 My first API
This is an API for getting historical currency ratings from 
NBP API completed with data for missing ratings. You can also 
access total sales data from provided database using this api.  
<br/>
**Quickstart**  
1. Install Python 3.7 or up on your computer: https://www.python.org/downloads/
2. Go to the downloaded project directory by running `cd <repo_address>`
3. `python -m pip install flask`
4. `python -m pip install Flask-Limiter`
5. Run `python api.py` to start the API  

**User manual**  
API requests return data in JSON format. Data is available for dates between 
2013-01-04 and 2016-12-29.  
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
- `/api/rates/{code}/{startDate}/{endDate}` returns specified currency rates 
in given time span with 'Interpolated' parameter. If {startDate} or {endDate}
is outside the supported range result contains rates from days within the supported
range.
- `/api/sales/{date}` returns sales from given day in USD and PLN and currency 
rate from given day. If no sales occurred on given day 'ERROR: No data found. Sales
 on given day totalled 0' is returned.
- `/api/sales/{startDate}/{endDate}` returns nonzero sales from given time span in USD 
and PLN and currency rate from given time span. If no sales occurred in given time span
 'ERROR: No data found. Sales on given days totalled 0' is returned.  
 
Request examples:
 - `http://127.0.0.1:5000/api/rates/USD/2014-03-01` returns USD exchange rate from 
1st March 2014.
- `http://127.0.0.1:5000/api/rates/PLN/2014-03-01/2014-03-30` returns PLN exchange rates from 1st March 2014
to 30th March 2014.
- `http://127.0.0.1:5000/api/sales/2015-10-01` returns sales from 1st October 2015 in USD and PLN and currency 
rate from that day.
- `http://127.0.0.1:5000/api/sales/2015-10-01/2015-11-01` returns nonzero sales from 1st October 2015 to 
1st November 2015 in USD and PLN and currency rate from given time span.
