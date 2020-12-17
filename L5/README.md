# Moje API

##
Moje API is used to get information on USD/PLN exchange rates in 2013-2016
and the value of total sales of products in those years

## Technologies
 - Python 3.7.4
    To install Python, visit https://www.python.org/downloads/
    You can check the Python version on the command line with the command: python --version
 - beep
    If you downloaded Python from the site above, it should be already installed.
    If you want to install pip, please visit https://pypi.org/project/pip/ or https://pip.pypa.io/en/stable/installing/
    You can check the pip version on the command line with the command: pip --version
 - Flask
 - Flask-Limiter
 - sqlite3
 - datetime
 - requests
    To install the missing libraries from the command line, type: pip install {library name}

## Launch
In order to start the application, run the api.py file.
You can do it, for example, in the command line with the command: python {path to api.py}
To verify, if the application is working correctly, go to http://127.0.0.1:5000/
A short api manual should appear on the page.

## Description of the API features
The site response is returned in JSON format.
The response code on success is 200.

### Request parameters
 - {date}, {start_date}, {end_date} - date in the format YYYY-MM-DD (ISO 8601 standard)

### Available requests
 - Request for dollar exchange rate on {date}:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/{date}/
 - Request for dollar exchange rates from {start_date} to {end_date}:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/{start_date}/{end_date}/
 - Request for total sales on {date}:
    http://127.0.0.1:5000/api/v1/salesdata/{date}/
 - Request for total sales from {start_date} to {end_date}:
    http://127.0.0.1:5000/api/v1/salesdata/{start_date}/{end_date}/

### Response parameters
 - date - exchange/sale date
 - interpolated - (true - approximate, value from recent known qutation; false - equal NBP rate)
 - PLN - total sales value in PLN
 - rate - exchange rate
 - USD - total sales value in US dollars

### Error messages
 - For a request with an unknown path structure, the response code is 404 and the following message is returned:
    The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
 - If the available number of queries per time unit is exceeded, the response code is 429 and the following message is returned:
    10 per 1 minute
 - For a request with a date outside the range, the following message is returned:
    404 NotFound - No data available
 - For a request containing an incorrect date format, the following message is returned:
    400 Bad Request - Invalid date format / Invalid date format
 - For a request containing an invalid date range, the following message is returned:
    400 BadRequest - Wrong date range / Invalid date range

### Time limits
For a given request, limit per time unit per user (IP address) is equal 10 / min.

### Other restrictions
In order to improve the program work, communication with the database is limited.
The received data may be out of date - the data refresh time is no more than an hour.

## Examples of use
 - Request for dollar exchange rate on 2015-12-12:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/2015-12-12/
 - Request for dollar exchange rates from 2014-01-01 to 2014-12-31:
    http://127.0.0.1:5000/api/v1/exchangerates/USD/2014-01-01/2014-12-31/
 - Request for total sales on 2016-03-20:
    http://127.0.0.1:5000/api/v1/salesdata/2016-03-20/
 - Request for total sales from 2013-01-01 to 2013-01-31:
    http://127.0.0.1:5000/api/v1/salesdata/2013-01-01/2013-01-31/

## Structure
The project consists of the following files:
 - api.py - a file with the code responsible for communication with the user,
 - sales_data_base.py - file with the code responsible for communication with the database,
 - sales_data.db - database file.

## Possible modifications

### Modification of the query limit per unit of time
In order to modify the query limit, in the api.py file, on line 26, change the text "10 per minute" to the target text.
Possible combinations: [count] [per | /] [n (optional)] [second | minute | hour | day | month | year]
Examples: "1 per second", "5 per 10 second", "100 per day"

### Modification of the maximum data storage time in the server cache
To modify the maximum time, change the fragment (hours=1) in the api.py file on line 10.
Examples: (minutes=1), (seconds=30), (days=7), (hours=2, minutes=30)
