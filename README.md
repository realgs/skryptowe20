# API Rates and Sales

## Introduction

My api is used to get the value of currencies rates and the total sales in a small Cortland store in 2020-2018.

## Running the server

Navigate to project directory and create virtual environment:

```sh
python -m venv venv
venv\Scripts\Activate
```

also you need to install following dependencies:
```
pip install django
pip install djangorestframework
```

Migrate and run application:
```sh
python manage.py migrate
python manage.py runserver
```

# Example API Usage

## Rates

For the convenience and testing of the application, I have set a default day if we do not provide parameters.

```sh
http://127.0.0.1:8000/rate
```

Returned data:
```js
{
    "ID": 214,
    "Date": "2019-05-11",
    "Rate USD": 3.8242,
    "Interpolated": true
}
```

If we want to choose a specific day, than:

```sh
http://127.0.0.1:8000/rate/{date}
```
Example:

```sh
http://127.0.0.1:8000/rate/2018-12-12
```
Returned data:

```js
{
    "ID": 64,
    "Date": "2018-12-12",
    "Rate USD": 3.7934,
    "Interpolated": false
}
```
If we want to choose a date range:

```sh
http://127.0.0.1:8000/rate/dates/{fromeDate}/{toDate}
```
Example:

```sh
http://127.0.0.1:8000/rate/dates/2019-06-15/2019-06-18
```
Returned data:
```js
[
    {
        "Date": "2019-06-15",
        "Rate": 3.7727,
        "Interpolated": "True"
    },
    {
        "Date": "2019-06-16",
        "Rate": 3.7727,
        "Interpolated": "True"
    },
    {
        "Date": "2019-06-17",
        "Rate": 3.7989,
        "Interpolated": "False"
    },
    {
        "Date": "2019-06-18",
        "Rate": 3.8097,
        "Interpolated": "False"
    }
]
```
## Sales

Total sales on the default date. (for quick testing)

```sh
http://127.0.0.1:8000/sales/
```
Returned data:
```js
{
    "ID": 522,
    "Date": "2019-05-07",
    "In PLN sales": 56163,
    "IN USD sales": 214980.73
}
```
If we want to choose a specific day, than:

```sh
http://127.0.0.1:8000/sales/{date}
```
Example:

```sh
http://127.0.0.1:8000/sales/2019-05-05
```

Returned data:
```js
{
    "ID": 524,
    "Date": "2019-05-05",
    "In PLN sales": 55449,
    "IN USD sales": 211687.65
}
```

If we want to choose a date range:
```sh
http://127.0.0.1:8000/sales/dates/{fromeDate}/{toDate}
```

Example:
```sh
http://127.0.0.1:8000/sales/dates/2019-05-25/2019-05-28
```

Returned data:
```js 
[
    {
        "Date": "2019-05-28",
        "USD Sales": 20965,
        "PLN Sales": 80476.25
    },
    {
        "Date": "2019-05-27",
        "USD Sales": 58194,
        "PLN Sales": 223313.66
    },
    {
        "Date": "2019-05-26",
        "USD Sales": 7527,
        "PLN Sales": 28930.78
    },
    {
        "Date": "2019-05-25",
        "USD Sales": 2745,
        "PLN Sales": 10550.68
    }
]
```

# Limits

Limits assigned to user. For an anon, it is 20 per hour, and for user is is 50 per hour. The limit settings are in the settings.py file.
