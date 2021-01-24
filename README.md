# Exchange Django REST API 

Stock exchange API based on Django-REST framework

## Getting Started

Clone repository on your machine

### Prerequisites

* [Python](https://www.python.org/downloads/) - Download version 3.7

Install Django framework:

```
$ python -m pip install Django
```

Install django-rest-framework:

```
$ pip install djangorestframework
$ pip install markdown       # Markdown support for the browsable API.
$ pip install django-filter  # Filtering support
```

### Installing

In root project directory run command:

```
python manage.py runserver
```

## Using API

To get rates records type:

```
http://127.0.0.1:8000/rates/
```

To get rates from period of time type:

```
http://127.0.0.1:8000/rates/2005-01-09/2005-04-10
```

To get volume from selected day:

```
http://127.0.0.1:8000/volume/2004-05-08
```

### Others

API "GET" requests are limited to 1 request per 2 seconds by user.

To run "insert_db_data.py" you need to add environment variable:

For Windows OS
```
SET DJANGO_SETTINGS_MODULE=Django_API.settings
```

For Unix OS (Linux, MacOS)
```
EXPORT DJANGO_SETTINGS_MODULE=Django_API.settings
```


