# README

### Installation

Install the dependencies and devDependencies and start the server.

```
$ pip3 install -r requirements.txt
$ cd migrations
$ python3 run_migrations.py
$ cd ..
$ python3 main.py
```

After this, api server by default will be available on  http://127.0.0.1:5000/

### API routes

* /api/exchangerates/?from=`X`&to=`Y`
-- `Method`:`GET`
-- `Returns`: currency rates in specified date range
-- `X`: left date range bound (inclusive) in format yyyy-mm-dd
-- `Y`: right date range bound (inclusive) in format yyyy-mm-dd

* /api/sales/?date=`X`
-- `Method`:`GET`
-- `Returns`: total sales in 2 currencies for specified date
-- `X`: date in format yyyy-mm-dd for which total sales in 2 currencies will be returned

### Request constraints

* Max 5 requests per minute
* Max 300 requests per hour
* Max 1000 request per day