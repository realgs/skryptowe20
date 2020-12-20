# Exchange rates api with sales data

This application provides an API that allows to check USD exchange rates and total sale of one online store in PLN and USD.

## What do you need?

### a)
You'll need python installed on your computer. I tested this project with python 3.9. You can download it from https://www.python.org/downloads/

### b)
Some python packages. All needed packages are in file requirements.txt. To install then you need to open terminal in cloned directory and type 
```bash
pip install -r requirements.txt
```

### c)
MySQL server. I recommend you XAMPP. You can get it from https://www.apachefriends.org/pl/download.html.

### d)
In this repo you have db.sql file. That is database with all API data. You can import it with MySQL Workbench.

## Run app
1. Run MySQL server with imported database
2. Run application by running api.py script.


## API endpoints
* /api/rates/usd/{date} - get exchange rate USD to PLN for one day
* /api/rates/usd/{start_date}/{end_date} - get exchange rate USD to PLN for period of days
* /api/sales/{date} - get store sales sum for one day in USD and PLN

## Returned data structure
### For exchange rates
Here for /api/rates/usd/2003-1-1/2003-01-04
```json
[
{
"date": "2003-01-01",
"interpolated": 1,
"rate": 3.84
},
{
"date": "2003-01-02",
"interpolated": 0,
"rate": 3.83
},
{
"date": "2003-01-03",
"interpolated": 0,
"rate": 3.84
},
{
"date": "2003-01-04",
"interpolated": 1,
"rate": 3.84
}
]
```
Interpolated 1 means that that day was for example weekend and banks didn't work. This value is a copy from last known non interpolated value.

### For sales
Here for /api/sales/2003-05-07
```json
{
"converted_pln": 63294.78,
"date": "2003-05-07",
"original_usd": 16700.47
}
```

##Limitations
API has limit for querying. For one IP you can make one request per second but max 30 requests per hour.

## Others
This API uses cache. That means when you refresh the page you get data from browser cache. The default timeout for cache is set to 60 seconds.