### SALES & CURRENCY EXCHANGE RATIO API

This API can be use to get exchange ratio of **PLN** (polish currency) and daily sales of company.
### INSTALLATION
First of all you will have to install **Python 3.8**
Official Python website: https://www.python.org
Also to use this app you will have to install those packets:
```

pip install requests
pip install Flask
pip install Flask-Limiter
pip install Flask-Cashing

```

### Cache

Cache saves information given to user, if user wants to get the same information it will be 
collected from Cache memory. Cache memory will last for **24 hours**.

### LIMITS

Daily limits = **100**
Hour-long limits = **15**

### HOW TO USE IT?

To start you will have to run ***API.py*** from console or IDE:
```
python API.py
```
Then go to ***http://127.0.0.1:5000/*** and insert text
To get exchange ratio use this pattern
```
http://127.0.0.1:5000/rates/<CURRENCY>/<BEGINING>/<END>/
```
or
```
http://127.0.0.1:5000/rates/<CURRENCY>/<CHOSEN_DATE>/
```
If ratio is from day before(or day before that day etc...) interpolated will **True**


To get sales use this pattern
```
http://127.0.0.1:5000/sales/<BEGINING>/<END>/
```
or
```
http://127.0.0.1:5000/sales/<CHOSEN_DATE>/
```
Output of sales will give date/pln/usd information.

Currency exchange ratio is from **NBP API**: http://api.nbp.pl
Sales u can get are between **2011-03-18** and **2013-07-11**

EXAMPLES
**INPUT**
```
http://127.0.0.1:5000/sales/2011-09-30/2011-10-30/
```
**OUTPUT**
```
{
  "2011-09-30": {
    "PLN": 45.15, 
    "USD": 13.86
  }, 
  "2011-10-08": {
    "PLN": 3.23, 
    "USD": 0.99
  }, 
  "2011-10-21": {
    "PLN": 6.33, 
    "USD": 1.98
  }, 
  "2011-10-22": {
    "PLN": 12.66, 
    "USD": 3.96
  }, 
  "2011-10-23": {
    "PLN": 18.99, 
    "USD": 5.94
  }, 
  "2011-10-26": {
    "PLN": 28.06, 
    "USD": 8.91
  }
}
```
**INPUT**
```
http://127.0.0.1:5000/rates/usd/2011-09-30/2011-10-02/
```
**OUTPUT**
```
{
"2011-09-30": {
    "interpolated": false, 
    "rate": 3.2574
  }, 
  "2011-10-01": {
    "interpolated": true, 
    "rate": 3.2574
  }, 
  "2011-10-02": {
    "interpolated": true, 
    "rate": 3.2574
  }
}
```
**INPUT**
```
http://127.0.0.1:5000/rates/usd/2011-09-30/
```
**OUTPUT**
```
{
  "2011-09-30": {
    "interpolated": false, 
    "rate": 3.2574
  }
}
```
