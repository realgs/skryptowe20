#!/bin/python3

from typing import Dict
import flask
from flask import Flask
from config import *
from sqlite3 import DatabaseError
from flask_limiter import Limiter
import datetime as dt
from dbhandler import Currency
import caching


app = Flask(__name__)

sales_sum_precached: Dict[Currency, Dict[dt.date, float]] = {}
if ENABLE_PRECACHING:
    sales_sum_precached[Currency.UNITED_STATES_DOLLAR] = caching.cache_sales_sum_original()
    for curr in Currency:
        if curr != Currency.UNITED_STATES_DOLLAR:
            sales_sum_precached[curr] = caching.cache_sales_sum(
                curr, sales_sum_precached[Currency.UNITED_STATES_DOLLAR])


@app.errorhandler(DatabaseError)
def db_exception_handler(error):
    return 'Database connection failed', 500


############    ROUTING     ####################

@app.route('/')
def index():
    pass


@app.route('/api/v1/rates/<currency_code>/all')
def get_rates_all(currency_code: str):
    pass


@app.route('/api/v1/rates/<currency_code>/day/<date>')
def get_rate_day(currency_code: str, date: str):
    pass


@app.route('/api/v1/rates/<currency_code>/range/<start_date>/<end_date>')
def get_rates_range(currency_code: str, start_date: str, end_date: str):
    pass


@app.route('/api/v1/sales/sum/<currency_code>/<date>')
def get_sales_sum_day(currency_code: str, date: str):
    pass


############    TESTS       ##############
if DEBUG_MODE:
    with app.test_request_context('/api/v1/rates/usd/day/2011-01-10?interpolated=1'):
        assert flask.request.args['interpolated'] == '1'


if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
