from flask import Flask, abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utilities_database import create_database, update_datebase
from utilities_api import universal_database_rates_call, get_sales_from_database
import argparse


# Config
app = Flask(__name__)
app.config["CACHE_TYPE"] = "simple"
cache = Cache()
cache.init_app(app)
DEFAULT_TIMEOUT = 60
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10000 per day", "100 per minute"]
)


# Interpolated
@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/inter/<string:code>/<int:last_days>')
def routing_interpolated_from_last_x_days(code, last_days):
    return universal_database_rates_call(code, True, last_days=last_days)


@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/inter/<string:code>/<string:single_date>')
def routing_interpolated_from_single_date(code, single_date):
    return universal_database_rates_call(code, True, from_date=single_date, till_date=single_date)


@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/inter/<string:code>/<string:from_date>/today')
def routing_interpolated_from_date_till_today(code, from_date):
    return universal_database_rates_call(code, True, from_date=from_date)


@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/inter/<string:code>/<string:from_date>/<string:till_date>')
def routing_interpolated_from_date_till_date(code, from_date, till_date):
    return universal_database_rates_call(code, True, from_date=from_date, till_date=till_date)


# Standard
@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/<string:code>/<int:last_days>')
def routing_from_last_x_days(code, last_days):
    return universal_database_rates_call(code, False, last_days=last_days)


@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/<string:code>/<string:single_date>')
def routing_from_from_single_date(code, single_date):
    return universal_database_rates_call(code, False, from_date=single_date, till_date=single_date)


@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/<string:code>/<string:from_date>/today')
def routing_from_date_till_today(code, from_date):
    return universal_database_rates_call(code, False, from_date=from_date)


@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/rates/<string:code>/<string:from_date>/<string:till_date>')
def routing_from_date_till_date(code, from_date, till_date):
    return universal_database_rates_call(code, False, from_date=from_date, till_date=till_date)


# Sales
@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/sales/<string:code>/<string:single_date>')
def routing_sales_single_date(code, single_date):
    return get_sales_from_database(code, single_date)


@cache.memoize(timeout=DEFAULT_TIMEOUT)
@app.route('/sales/<string:code>/<string:from_date>/<string:till_date>')
def routing_sales_period(code, from_date, till_date):
    return get_sales_from_database(code, from_date, till_date)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--set-up', action='store_true') 
    parser.add_argument('--run', action='store_true') 
    args = parser.parse_args()
    if args.set_up:
        create_database()
    if args.update:
        update_datebase()
    if args.run:
        app.run()
