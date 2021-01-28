from datetime import datetime

from flask import jsonify, abort, render_template
from flask_cors import CORS, cross_origin
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from lab5_solutions.database_repository import *

TWENTY_FOUR_HOURS = 24 * 60 * 60

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": TWENTY_FOUR_HOURS
}

app = flask.Flask(__name__, static_folder='../frontend/dist/', static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_mapping(config)

cache = Cache(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["500 per day", "30 per hour"]
)


# def limit_per_all():
#     return "0"

# shared_limit = limiter.shared_limit("50/hour", scope="api", key_func=limit_per_all, override_defaults=False)

def __check_currency(currency):
    for curr in Currency:
        if currency == curr.value:
            return True
    abort(400, description="This currency is not supported: '{}'.".format(currency))


def __check_date(date):
    if date > MAX_DATE or date < MIN_DATE:
        abort(400, description="Date must be in range: from '{}' to '{}'.".format(MIN_DATE, MAX_DATE))


def __check_date_range(start_date, end_date):
    date_diff = (end_date - start_date).days
    if date_diff < 0:
        abort(400, description="Start date: '{}' cannot be after the end date: '{}'.".format(start_date, end_date))


def __date_string_to_datetime_converter(date_string):
    try:
        return datetime.strptime(date_string, format(DATE_FORMAT)).date()
    except ValueError:
        abort(400, description="Invalid date format: '{}'.".format(date_string))


@app.route('/')
@cross_origin()
def home():
    return app.send_static_file('index.html')


@app.route('/exchange-rates/<currency>/<date>', methods=['GET'])
# @shared_limit
@cross_origin()
@cache.cached()
def rate_one_day(currency, date):
    return rate_from_date_to_date(currency, date, date)


@app.route('/exchange-rates/<currency>/<start_date>/<end_date>', methods=['GET'])
# @shared_limit
@cross_origin()
@cache.cached()
def rate_from_date_to_date(currency, start_date, end_date):
    __check_currency(currency)
    start_date_dt = __date_string_to_datetime_converter(start_date)
    end_date_dt = __date_string_to_datetime_converter(end_date)
    __check_date(start_date_dt)
    __check_date(end_date_dt)
    __check_date_range(start_date_dt, end_date_dt)

    return jsonify(rates=select_rate_between_dates(currency, start_date, end_date))


@app.route('/sales/<date>', methods=['GET'])
# @shared_limit
@cross_origin()
@cache.cached()
def sale_one_day(date):
    return sale_from_date_to_date(date, date)


@app.route('/sales/<start_date>/<end_date>', methods=['GET'])
# @shared_limit
@cross_origin()
@cache.cached()
def sale_from_date_to_date(start_date, end_date):
    start_date_dt = __date_string_to_datetime_converter(start_date)
    end_date_dt = __date_string_to_datetime_converter(end_date)
    __check_date(start_date_dt)
    __check_date(end_date_dt)
    __check_date_range(start_date_dt, end_date_dt)
    sales = select_sale_between_dates(start_date, end_date)
    if sales == []:
        sales = [{'date': start_date, 'usd': 0, 'pln': 0}]

    return jsonify(sales=sales)


@app.teardown_appcontext
def close_database_connection(exception):
    close_connection(exception)


if __name__ == '__main__':
    app.run()
