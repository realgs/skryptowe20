from flask import Flask, jsonify, abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import argparse
import sqlite3

from database import database
from nbp_api import nbp_api

TIME = 365 * 20

CURRENCIES = ['eur', 'usd', 'gbp']
DATE_FORMAT = nbp_api.DATE_FORMAT

app = Flask(__name__)
config = {
    'DEBUG': True,
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
}
app.config.from_mapping(config)
limiter = Limiter(app,key_func=get_remote_address,default_limits=["200 per day", "50 per hour"])
cache = Cache(app)


@app.errorhandler(sqlite3.OperationalError)
def handle_exception(e):
    return jsonify({'error': 'unsupported currency'}), 400


@app.errorhandler(ValueError)
def handle_exception(e):
    return jsonify({'error': 'check your input, probably date is in wrong format'}), 400


@app.route('/currency/<currency>/time/today')
@cache.memoize()
def get_retes_of_currency_from_today(currency):
    today = datetime.today()
    db = database()
    return jsonify(db.get_currency_between(currency, today, today))


@app.route('/currency/<currency>/time/<day>')
@cache.cached()
def get_retes_of_currency_from_given_day(currency, day):
    db = database()
    day_parsed = datetime.strptime(day, DATE_FORMAT)
    return jsonify(db.get_currency_between(currency, day_parsed, day_parsed))


@app.route('/currency/<currency>/time/<begin>/<end>')
@cache.cached()
def get_retes_of_currency_between(currency, begin, end):
    db = database()
    begin_parsed = datetime.strptime(begin, DATE_FORMAT)
    end_parsed = datetime.strptime(end, DATE_FORMAT)
    return jsonify(db.get_currency_between(currency, begin_parsed, end_parsed))


@app.route('/currency/<currency>/last/<int:days>')
@cache.cached()
def get_retes_of_currency_last_days(currency, days):
    db = database()
    return jsonify(db.get_currency(currency, days))


@app.route('/sales/<currency>/time/<day>')
@cache.cached()
def get_sales_from_given_day(currency, day):
    db = database()
    day_parsed = datetime.strptime(day, DATE_FORMAT)
    return jsonify(db.get_sales_between(currency, day_parsed, day_parsed))


@app.route('/sales/<currency>/time/<begin>/<end>')
@cache.cached()
def get_sales_between(currency, begin, end):
    db = database()
    begin_parsed = datetime.strptime(begin, DATE_FORMAT)
    end_parsed = datetime.strptime(end, DATE_FORMAT)
    return jsonify(db.get_sales_between(currency, begin_parsed, end_parsed))


def init_server_database():
    db = database()
    for currency in CURRENCIES:
        db.create_currency_table(currency, TIME)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', help='init database', action='store_true', default=False)
    args = parser.parse_args()
    if args.init:
        init_server_database()
    app.run()
