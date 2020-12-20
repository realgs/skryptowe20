#!/bin/python3

from typing import Dict
import flask
from flask import Flask
from werkzeug.exceptions import InternalServerError
from config import *
from sqlite3 import DatabaseError
from flask_limiter import Limiter
import datetime as dt
from dbhandler import Currency
import caching


############    EXCEPTIONS      ##############
class DateFormatError(Exception):
    pass


class OutOfRangeError(Exception):
    pass


class CurrencyCodeError(Exception):
    pass


class NoCurrencyError(Exception):
    pass

############    MISC    ##############
def validate_currency_code(code: str) -> bool:
    return code.isalpha() and len(code) == 3


sales_sum_precached: Dict[Currency, Dict[dt.date, float]] = {}
if ENABLE_PRECACHING:
    sales_sum_precached[Currency.UNITED_STATES_DOLLAR] = caching.cache_sales_sum_original()
    sales_sum_precached[Currency.POLISH_ZLOTY] = caching.cache_sales_sum(
        Currency.POLISH_ZLOTY, sales_sum_precached[Currency.UNITED_STATES_DOLLAR])


############    API   #################


app = Flask(__name__)


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


@app.errorhandler(InternalServerError)
def handle_500(error):
    return {'error': type(error).__name__, 'message': '500 Internal Server Error'}, 500


############    ROUTING     ####################

@app.route('/')
def index():
    return ''


@app.route('/api/v1/rates/<currency_code>/all')
def get_rates_all(currency_code: str):
    if not validate_currency_code(currency_code):
        raise CurrencyCodeError


@app.route('/api/v1/rates/<currency_code>/day/<date>')
def get_rate_day(currency_code: str, date: str):
    pass


@app.route('/api/v1/rates/<currency_code>/range/<start_date>/<end_date>')
def get_rates_range(currency_code: str, start_date: str, end_date: str):
    pass


@app.route('/api/v1/sales/sum/<date>')
def get_sales_sum_day(date: str):
    pass


############    TESTS       ##############
if DEBUG_MODE:
    with app.test_request_context('/api/v1/rates/usd/day/2011-01-10?interpolated=1'):
        assert flask.request.args['interpolated'] == '1'


if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
