# Forex&Sales API
Welcome

## What is it?
It is an API made to serve sales and forex data. It's based on NBP's (http://api.nbp.pl/) data and uses a mock database to present its capabilities.

## Technologies
To make it simple, only simple technologies. These include:
* [Python](https://www.python.org/dwonloads/) programming language (version **3.7.4** or higher)
* [Flask framework](https://flask.palletsprojects.com/en/1.1.x/) - an API service framework
* [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/) - a server-load limiter extension to Flask
* [sqlite3](https://www.sqlite.org/index.html) - a database engine
* [requests](https://requests.readthedocs.io/en/master/) - an API client framework (to obtain data from NBP's database)

## Project struucture
* `main.py` - the file to launch the whole service
* `api.py` - the API service script
* `database.py` - a script for connecting with the database
* `currency_API.py` - a client for NBP API, implementing the *requests* framework
* `sales_data.db` - a mock database
* `README.md` - what you are reading right now

## How can I get it working?
1. Start with obtaining python (it comes preinstalled with MacOS) - if you don't have it yet, you can download and install from https://www.python.org/dwonloads/. Remember to get **3.7.4** or higher. It should come together with pip - it's a package manager that enables you to download all the other necessary libraries.
2. Check your python installation with `python --version` in your command line. Also, check pip using a similar command, `pip --version`. If somehow pip doesn't seem be there, you can get it following instructions on https://pip.pypa.io/en/stable/installing/.
3. Now you can proceed to obtaining specific packages. Use `pip install {library_name}` for each one that is missing (see **Technologies** above). You can list already installed packages launching python in command line (simply with `python`) and running `help("modules")`.
4. Once you've gone thru the installation process, you can launch the application with a command `python main.py`. Make sure to go into the installation (or cloned repo) directory first, or use a global file path instead, e.g. `~/documents/Forex&Sales API/main.py`.
5. If it's running properly, you'll be able to see in the console where the service is running - typically it's `localhost:5000`. What's more, in the console it's about to appear every single request made to the API.
6. That's it! Go to `localhost:5000` and check it.

## How do I use it?
There are actually 2 ways of using it.
* Get currency markings - it uses the `/api/v1/exchangerates/` URI
* Get currency markings - it uses the `/api/v1/salesdata/` URI
Apart from that you can also visit homepage (`/`) or ping (`/ping`) the API to check if it's responding.

### Request parameters
- `{top_count}` is an *integer* value, **greater or equal to 0**; it is the number of pieces of data provided in the response ;if  the value exceeds number of available items of request, a maximum amount is returned as the first item
- `{date}`, `{start_date}`, `{end_date}` are dates of the `YYYY-MM-DD` format defined by the [ISO 8601](http://pl.wikipedia.org/wiki/ISO_8601) standard; in addition, {start_date} should be greater or equal to {end_date}; a single `{date}` is the day of data to be requested, while `{start_date}` and `{end_date}` define respectively the start and the end of the requested period of time
- `{currency_code}` - a **3-letter** code uniquely representing the currency, defined by standard [ISO 4217](http://pl.wikipedia.org/wiki/ISO_4217)

### Getting currency markings
You can request available forex tables in various configurations.

* all available currencies data (`{currency}/PLN`)
    * `/api/v1/exchangerates/tables/` - request for all available forex data
    * `/api/v1/exchangerates/tables/today` - request for all available forex data of today
    * `/api/v1/exchangerates/tables/last/{top_count}` - request for all available forex data, limited by `{top_count}`
    * `/api/v1/exchangerates/tables/{date}` - request for all available forex data of the provided `{date}`
    * `/api/v1/exchangerates/tables/{start_date}/{end_date}` - request for all available forex data of the period of time between provided `{start_date}` and `{end_date}`
* specific currency data (`{currency}/PLN`)
    * `/api/v1/exchangerates/rates/{currency_code}/` - request for all available `{currency_code}` data
    * `/api/v1/exchangerates/rates/{currency_code}/today` - request for all available `{currency_code}` data of today
    * `/api/v1/exchangerates/rates/{currency_code}/last/{top_count}` - request for all available `{currency_code}` data, limited by `{top_count}`
    * `/api/v1/exchangerates/rates/{currency_code}/{date}` - request for all available `{currency_code}` data of the provided `{date}`
    * `/api/v1/exchangerates/rates/{currency_code}/{start_date}/{end_date}` - request for all available `{currency_code}` data of the period of time between provided `{start_date}` and `{end_date}`

### Geting sales data
* `/api/v1/salesdata/{date}` - request for all available sales data of the provided `{date}`
* `/api/v1/salesdata/{start_date}/{end_date}` - request for all available sales data of the period of time between provided `{start_date}` and `{end_date}`

### Possible response formats
* a **marking** request results in a list of or a single JSON object of the structure
    ``` JSON
    {
        'date' : {date},
        'rate' : {rate},
        'currency' : {currency_code},
        'interpolated' : {true | false}
    }
    ```
    - `date` is the date that the data applies to
    - `rate` is the value of the `{currency_code}/PLN` marking
    - `currency` is the `{currency_code}` requested, or one of the response of a `tables` request
    - `interpolated` - determines whether the rate is accurate (false) or aproximated (true) using data from the previous days
* if the value exceeds number of available items of request, a maximum amount is returned as the first item: `{'markings served' : {markings_served}}`

* a **sales** request evaluates to a list of or a single JSON object of the structure
``` JSON
    {
        'date' : {date},
        'PLN' : {value},
        {currency} : {value},
        …
    }
```
- `date` is the date that the data applies to
- `PLN` is the total value of the sales in **PLN**
- `currency` is the total value of the sales in `{currency_code}`; listed for every currency data available for the `date`

### Possible error messages
Error message is a JSON response coded as follows:
```JSON
    {
        'error':
        {
            'code' : {code},
            'message' : {message}
        }
    }
```
where `{code}` is the HTTP response code and `{message}` is the message telling what went wrong with the request.

Meaning of error messages
* General request errors
    * 400: Bad request.
    * 403: You don't have permission to the resource.
    * 404: The resource could not be found.
    * 429: Limit of requests exceeded.
    * 500: Internal server error. Please try again later.
* Service specific messages
    * 400: Invalid request parameters (see *Request parameters* above).
    * 404: No data available for the request.

## Deeper configuration
In scripts `currency_API.py` and `database.py` a wide variety of commands can be found, so that you can use them combined together in order to provide other currency data or even another database. Just place the function calls in `main.py` near (or instead of) basic configuration. Furthermore, in the `api.py` file following preferences might be changed:
* `TABLES_URI` - this represents the URI used for currency requests
* `RATES_URI` - this represents the URI used for specific currency requests
* `SALES_URI` - this represents the URI used for sales requests
* `DAILY_LIMIT`,  `MINUTE_LIMIT` - exemplary limits, used together few lines below in `default_limits = [DAILY_LIMIT, MINUTE_LIMIT]` - it can be any value following  the rule: `[count] [per|/] [n (optional)] [second|minute|hour|day|month|year]`; defaults are `200 per day` and `30 per minute` per an IP address
* `CACHE_LIFETIME` - how long [in seconds] the calculated sales data is supposed to be cached on the API server; default is `120`.

## Closing remarks
This is a personal project for university classes. It's not planned to be developed further. If you'd like the author to do so, set up an issue or whatever you want, just to let them know. Feel free to fork and request pulls.
