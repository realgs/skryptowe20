from flask import Flask, jsonify, abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import datetime, NoSuchTableError

import database as db
from keys import *

app = Flask(__name__)
config = {
    'DEBUG': True,
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
}
app.config.from_mapping(config)
cache = Cache(app)

time = 365 * 20
currencies = ['eur', 'usd']

def __get_rates_between_handler(currency, begin, end):
    res = db.get_rates_between(currency, begin, end)
    if(len(res) > 0):
        return jsonify(res)
    else:
        abort(400, 'Could not find anything in given period')

def __get_rates_last_handler(currency, delta):
    res = db.get_rates_last(currency, delta)
    if(len(res) > 0):
        return jsonify(res)
    else:
        abort(500, 'No records in database, sorry for the inconvenience')

def __get_sales_between_handler(currency, begin, end):
    res = db.get_sales_between(currency, begin, end)
    if(len(res) > 0):
        return jsonify(res)
    else:
        abort(400, 'Could not find anything in given period')

def __error_handler(function, *args):
    try:
        return function(*args)
    except TypeError:
        abort(400, 'Wrong types of paramters')
    except ValueError:
        abort(400, 'Invalid value of parameters')
    except NoSuchTableError:
        abort(400, 'Unsupported currency')

@app.route('/currency/<currency>/time/today')
@cache.memoize()
def get_retes_of_currency_from_today(currency):
    today = datetime.today().strftime(DATE_FORMAT)
    return __error_handler(__get_rates_between_handler, currency, today, today)

@app.route('/currency/<currency>/time/<day>')
@cache.cached()
def get_retes_of_currency_from_given_day(currency, day):
    return __error_handler(__get_rates_between_handler, currency, day, day)

@app.route('/currency/<currency>/time/<begin>/<end>')
@cache.cached()
def get_retes_of_currency_between(currency, begin, end):
    return __error_handler(__get_rates_between_handler, currency, begin, end)

@app.route('/currency/<currency>/last/<int:days>')
@cache.cached()
def get_retes_of_currency_last_days(currency, days):
    return __error_handler(__get_rates_last_handler, currency, days)

@app.route('/sales/<currency>/time/<day>')
@cache.cached()
def get_sales_from_given_day(currency, day):
    return __error_handler(__get_sales_between_handler, currency, day, day)

@app.route('/sales/<currency>/time/<begin>/<end>')
@cache.cached()
def get_sales_between(currency, begin, end):
    return __error_handler(__get_sales_between_handler, currency, begin, end)

if __name__ == "__main__":
    # for currency in currencies:
    #     db.create_and_fill_rates_table(currency, time)

    app.run()
