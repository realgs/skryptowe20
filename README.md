# API docs
## Instalation
Required python packages:
- numpy

Other requirements

## Setup
Preparing the database:
1. do sth
2. do sth else

Starting the API server:
1. Run manage.py located in Lab5/myApi with runserver argument, like so:

*python manage.py runserver*

## Usage
Supported API requests:

*/rates/{**currency**}/{**start_date**}/{**end_date**}/*

Where:
- **currency** -> ISO compliant currency code,
- **start_date** -> beginning of period, in format YYYY-MM-DD,
- **end_date** -> end of period, in format YYYY-MM-DD,
- start_date has to be smaller than end_date,
- max period is ....

Sample output:

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

Where:
- **interpolated** -> whether the value is estimated from previous days or not.

Status codes:
- **200** - SUCCESS
- **XXX** - WRONG DATE
- **XXX** - WRONG CODE

Tutorial:
https://docs.djangoproject.com/en/3.1/intro/tutorial01/