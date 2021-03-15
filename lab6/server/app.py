#!/bin/python3

from flask import Flask, request, redirect
from flask.json import jsonify
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import InternalServerError
from sqlite3 import DatabaseError

import datetime as dt
from typing import Any, Dict, List, Tuple

import caching
import dbhandler
from config import *
from dbhandler import Currency, DATE_FORMAT, currencyCodes


############    EXCEPTIONS      ##############
class DateFormatError(Exception):
    pass


class OutOfRangeError(Exception):
    pass


class RangeOrderError(Exception):
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


def convert_to_currency(code: str) -> Currency:
    if not validate_currency_code(code):
        raise CurrencyCodeError
    code = code.upper()
    if code in currencyCodes:
        curr = currencyCodes[code]
        if curr == Currency.POLISH_ZLOTY:
            raise NoCurrencyError
    else:
        raise NoCurrencyError
    return curr


def convert_to_date(date: str) -> dt.date:
    try:
        date_obj = dt.datetime.strptime(date, DATE_FORMAT).date()
        min_date, max_date = minmax_rates_date()
        if date_obj > max_date or date_obj < min_date:
            raise OutOfRangeError
    except ValueError:
        raise DateFormatError
    return date_obj


def get_interpolated_param() -> bool:
    query_parameters = request.args
    interpolated = False
    try:
        if 'interpolated' in query_parameters:
            interpolated = bool(int(query_parameters['interpolated']))
    except ValueError:
        raise InterpolatedParamError
    return interpolated


def get_sales_day(date: dt.date) -> Dict[str, Any]:
    sales_data: Dict[str, Any] = {}

    if date in precached_sales_sum_org():
        sales_sum_org = precached_sales_sum_org()[date]
        sales_sum_exch = precached_sales_sum_exch()[date]['sum']
        sales_sum_exch_rate = precached_sales_sum_exch()[date]['rate']
    else:
        sales_sum_org = 0
        sales_sum_exch = 0
        sales_sum_exch_rate = 'N/A'

    sales_data = {'date': date.strftime(DATE_FORMAT),
                  'original_value': sales_sum_org, 'exchanged_value': sales_sum_exch,
                  'exchange_rate': sales_sum_exch_rate}

    return sales_data


############    API   #################
config = {
    "DEBUG": DEBUG_MODE,          # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 0  # cache never expires
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

limiter = Limiter(app, key_func=get_remote_address, enabled=ENABLE_LIMITER)


@cache.memoize()
def minmax_rates_date() -> Tuple[dt.date, dt.date]:
    print('Pre-caching query. It may take a while...')
    return dbhandler.query_minmax_date()


@cache.memoize()
def precached_sales_sum_org() -> Dict[dt.date, float]:
    print('Pre-caching query. It may take a while...')
    return caching.cache_sales_sum_original()


@cache.memoize()
def precached_sales_sum_exch() -> Dict[dt.date, Dict[str, float]]:
    print('Pre-caching query. It may take a while...')
    return caching.cache_sales_sum_exchanged(
        Currency.UNITED_STATES_DOLLAR)


minmax_rates_date()
precached_sales_sum_exch()
precached_sales_sum_org()

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


@app.errorhandler(RangeOrderError)
def date_exception_handler(error):
    return {'error': type(error).__name__, 'message': 'Dates are in wrong order. End date must be after/equal start date.'}, 422


@app.errorhandler(InternalServerError)
def handle_500(error):
    return {'error': type(error).__name__, 'message': '500 Internal Server Error'}, 500


############    ROUTING     ####################

@app.route('/', methods=['GET'])
@limiter.limit(INDEX_LIMIT)
def index():
    return redirect(f'http://{FRONT_ADDRESS}:8080')


@app.route('/api/v1/rates/<currency_code>/all', methods=['GET'])
@limiter.limit(GET_RATES_ALL_LIMIT)
def get_rates_all(currency_code: str):
    interpolated = get_interpolated_param()
    curr = convert_to_currency(currency_code)

    return jsonify(dbhandler.query_rates_all(curr, interpolated))


@app.route('/api/v1/rates/<currency_code>/day/<date>', methods=['GET'])
@limiter.limit(GET_RATE_DAY_LIMIT)
def get_rate_day(currency_code: str, date: str):
    interpolated = get_interpolated_param()
    curr = convert_to_currency(currency_code)
    date_obj = convert_to_date(date)

    return jsonify(dbhandler.query_rate(curr, date_obj, interpolated))


@app.route('/api/v1/rates/<currency_code>/range/<start_date>/<end_date>', methods=['GET'])
@limiter.limit(GET_RATES_RANGE_LIMIT)
def get_rates_range(currency_code: str, start_date: str, end_date: str):
    interpolated = get_interpolated_param()
    curr = convert_to_currency(currency_code)
    start_date_obj = convert_to_date(start_date)
    end_date_obj = convert_to_date(end_date)

    if end_date_obj < start_date_obj:
        raise RangeOrderError

    return jsonify(dbhandler.query_rates_range(curr, start_date_obj, end_date_obj, interpolated))


@app.route('/api/v1/sales/sum/<date>', methods=['GET'])
@limiter.limit(GET_SALES_SUM_DAY_LIMIT)
def get_sales_sum_day(date: str):
    date_obj = convert_to_date(date)
    return jsonify(get_sales_day(date_obj))


@app.route('/api/v1/sales/sum/range/<start_date>/<end_date>', methods=['GET'])
@limiter.limit(GET_SALES_SUM_DAY_LIMIT)
def get_sales_sum_range(start_date: str, end_date: str):
    start_date_obj = convert_to_date(start_date)
    end_date_obj = convert_to_date(end_date)
    sales: List[Dict[str, Any]] = []

    if end_date_obj < start_date_obj:
        raise RangeOrderError

    if start_date_obj == end_date_obj:
        sales.append(get_sales_day(start_date_obj))
    else:
        for x in range((end_date_obj - start_date_obj).days + 1):
            tmp_date = start_date_obj + dt.timedelta(days=x)
            sales.append(get_sales_day(tmp_date))

    return jsonify(sales)


if __name__ == '__main__':
    app.run()
