# Store database API support

An application that allows you to download currency rates and the total daily turnover from the store database using the API

## Installation

### Required for the project to run

pyodbc=4.0.30
request=2.25.1
Flask=1.1.2
Flask-RESTful=0.3.8
Flask-Limiter=1.4

## Usage

### Useful information

By default, the application starts at: http://127.0.0.1:5000/
Default port: 5000
Date format: YYYY-MM-DD (e.g. 2020-01-01)
Currency format: XXX (e.g. USD)

### Available API functionalities

##### Retrieving the exchange rate for a date range
.../rates/<currency>/<date_from>/<date_to>

##### Daily turnover data download
.../turnover/<date>/<currency>
