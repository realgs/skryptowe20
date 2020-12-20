#!/bin/python3

from typing import Dict, Tuple
import flask
from flask import Flask, request
from werkzeug.exceptions import InternalServerError
from config import *
from sqlite3 import DatabaseError
from flask_limiter import Limiter
import datetime as dt
from dbhandler import Currency, DATE_FORMAT, currencyCodes
import dbhandler
import caching
from flask_caching import Cache


############    EXCEPTIONS      ##############
class DateFormatError(Exception):
    pass


class OutOfRangeError(Exception):
    pass


class CurrencyCodeError(Exception):
    pass


class NoCurrencyError(Exception):
    pass


class InterpolatedParamError(Exception):
    pass

############    MISC    ##############


def validate_currency_code(code: str) -> bool:
    return code.isalpha() and len(code) == 3


sales_sum_precached: Dict[Currency, Dict[dt.date, float]] = {}
sales_sum_precached[Currency.UNITED_STATES_DOLLAR] = caching.cache_sales_sum_original()
sales_sum_precached[Currency.POLISH_ZLOTY] = caching.cache_sales_sum(
    Currency.POLISH_ZLOTY, sales_sum_precached[Currency.UNITED_STATES_DOLLAR])


############    API   #################
config = {
    "DEBUG": DEBUG_MODE,          # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@cache.cached(timeout=180, key_prefix='minmax_rates')
def minmax_rates_date() -> Tuple[dt.date, dt.date]:
    return dbhandler.query_minmax_date()


############    ERROR HANDLING  ##############

@app.errorhandler(DatabaseError)
def db_exception_handler(error):
    return {'error': type(error).__name__, 'message': 'Database connection failed. Please contact server administrator.'}, 500


@app.errorhandler(DateFormatError)
def date_exception_handler(error):
    return {'error': type(error).__name__, 'message': 'Invalid date argument. Date has to be passed in given format: YYYY-MM-DD'}, 422


@app.errorhandler(OutOfRangeError)
def date_exception_handler(error):
    return {'error': type(error).__name__, 'message': 'Requested range exceedes the maximum range available in database.'}, 422


@app.errorhandler(CurrencyCodeError)
def date_exception_handler(error):
    return {'error': type(error).__name__, 'message': 'Invalid currency code. Valid code should consist of 3 letters'}, 422


@app.errorhandler(NoCurrencyError)
def date_exception_handler(error):
    return {'error': type(error).__name__, 'message': 'Requested currency is not available in database.'}, 422

@app.errorhandler(InterpolatedParamError)
def date_exception_handler(error):
    return {'error': type(error).__name__, 'message': 'Invalid argument value - interpolated should be set as 0 or 1'}, 422


@app.errorhandler(InternalServerError)
def handle_500(error):
    return {'error': type(error).__name__, 'message': '500 Internal Server Error'}, 500


############    ROUTING     ####################

@app.route('/', methods=['GET'])
def index():
    return ''


@app.route('/api/v1/rates/<currency_code>/all', methods=['GET'])
def get_rates_all(currency_code: str):
    if not validate_currency_code(currency_code):
        raise CurrencyCodeError
    currency_code = currency_code.upper()
    if currency_code in currencyCodes:
        curr = currencyCodes[currency_code]
    else:
        raise NoCurrencyError


@app.route('/api/v1/rates/<currency_code>/day/<date>', methods=['GET'])
def get_rate_day(currency_code: str, date: str):
    query_parameters = request.args
    interpolated = False
    try:
        if 'interpolated' in query_parameters:
            interpolated = bool(int(query_parameters['interpolated']))
    except ValueError:
        raise InterpolatedParamError

    if not validate_currency_code(currency_code):
        raise CurrencyCodeError
    currency_code = currency_code.upper()
    if currency_code in currencyCodes:
        curr = currencyCodes[currency_code]
        if curr == Currency.POLISH_ZLOTY:
            raise NoCurrencyError
    else:
        raise NoCurrencyError
    try:
        date_obj = dt.datetime.strptime(date, DATE_FORMAT).date()
        min_date, max_date = minmax_rates_date()
        if date_obj > max_date or date_obj < min_date:
            raise OutOfRangeError
    except ValueError:
        raise DateFormatError

    return flask.jsonify(dbhandler.query_rate(curr, date_obj, interpolated))


@app.route('/api/v1/rates/<currency_code>/range/<start_date>/<end_date>', methods=['GET'])
def get_rates_range(currency_code: str, start_date: str, end_date: str):
    pass


@app.route('/api/v1/sales/sum/<date>', methods=['GET'])
def get_sales_sum_day(date: str):
    pass


############    TESTS       ##############
if DEBUG_MODE:
    with app.test_request_context('/api/v1/rates/usd/day/2011-01-10?interpolated=1'):
        assert flask.request.args['interpolated'] == '1'


if __name__ == '__main__':
    app.run()
