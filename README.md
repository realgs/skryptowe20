# Instalation
Required python packages:
- asgiref==3.3.1
- certifi==2020.12.5
- chardet==3.0.4
- Django==3.1.4
- djangorestframework==3.12.2
- idna==2.10
- pytz==2020.4
- requests==2.25.0
- sqlparse==0.4.1
- urllib3==1.26.2

All above packages are listed in *requirements.txt*, ready to be imported with python.
# Setup
## Preparing the database:
1. Make sure the path to the database is correct in `constants.py`
2. The database will prepare on start of the server

## Starting the API server:
1. Run `manage.py` located in Lab5/myApi with runserver argument, like so:

`python manage.py runserver`

# Usage
## Exchange rates history
Data is fetched from nbpAPI. Supports all currencies supported by nbpAPI (listed in `constants.py`).


`/rates/{currency}/{start_date}/{end_date}/`

Where:
- `currency` -> ISO compliant currency code,
- `start_date` -> beginning of period, in format YYYY-MM-DD,
- `end_date` -> end of period, in format YYYY-MM-DD,

For example: `/rates/USD/2020-01-01/2020-10-10/`

Sample output:
```json
{
   "currency":"USD",
   "rates":[
      {
         "date":"2020-12-01",
         "value":"3.736",
         "interpolated":"false"
      },
      {
         "date":"2020-12-02",
         "value":"3.87",
         "interpoalted":"false"
      }
   ]
}
```
Where:
- **interpolated** -> whether the value is estimated from previous days or not.

## Transactions summary
Data is calculated during database preparation on setup. Due to used database's dataset, the date is bounded between 2012-07-04 and 2016-02-19 (listed in `constants.py`).

`/summary/{currency}/{date}/`

Where:
- `currency` -> supported currency code, specified as `SUMMARY_SUPPORTED_CURRENCIES` in `constants.py`,
- `date` -> day to summarise, in format YYYY-MM-DD,

For example: `/summary/USD/2015-12-18/`

Sample output:
```json
{
   "date":"2016-02-18",
   "original_sum":"202602.31",
   "currency_sum":"798577.27"
}
```
Where:
- **original_sum** -> sum of all transactions in the original value.
- **currency_sum** -> sum of all transactions in the requested currency.
