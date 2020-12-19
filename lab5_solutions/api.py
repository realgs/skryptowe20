import flask
from flask import request, jsonify
from lab5_solutions.database_repository import *
from datetime import datetime, date
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = flask.Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per day", "2 per hour"]
    # 1. version
)
shared_limit = limiter.shared_limit("5/hour", scope="api")  # 2. version

@app.route('/exchange-rates/<currency>/<date>', methods=['GET'])
@shared_limit
@limiter.limit('4 per hour')
@cache.cached()
def rate_one_day(currency, date):
    try:
        date_dt = datetime.strptime(date, format(DATE_FORMAT)).date()
        if date_dt > MAX_DATE or date_dt < MIN_DATE:
            return jsonify(cause="Date out of the date range."), 400
    except ValueError:
        return jsonify(cause="Invalid date format."), 400

    return jsonify(rates=select_rate_one_day(currency, date))


@app.route('/exchange-rates/<currency>/<start_date>/<end_date>', methods=['GET'])
@shared_limit
@cache.cached()
def rate_from_date_to_date(currency, start_date, end_date):
    try:
        start_date_dt = datetime.strptime(start_date, format(DATE_FORMAT)).date()
        end_date_dt = datetime.strptime(end_date, format(DATE_FORMAT)).date()
        if start_date_dt > MAX_DATE or start_date_dt < MIN_DATE:
            return jsonify(cause="Start date out of the date range."), 400
        if end_date_dt > MAX_DATE or end_date_dt < MIN_DATE:
            return jsonify(cause="End date out of the date range."), 400
        if end_date_dt < start_date_dt:
            return jsonify(couse="End date before start date."), 400
    except ValueError:
        return jsonify(cause="Invalid date format."), 400

    return jsonify(rates=select_rate_between_dates(currency, start_date, end_date))


@app.route('/sales/<currency>/<date>', methods=['GET'])
@shared_limit
@cache.cached()
def sale_one_day(currency, date):
    try:
        date_dt = datetime.strptime(date, format(DATE_FORMAT)).date()
        if date_dt > MAX_DATE or date_dt < MIN_DATE:
            return jsonify(cause="Date out of the date range."), 400
    except ValueError:
        return jsonify(cause="Invalid date format."), 400

    return jsonify(sales=get_sale_in_USD_PLN_one_day(currency, date))


@app.route('/sales/<currency>/<start_date>/<end_date>', methods=['GET'])
@shared_limit
@cache.cached()
def sale_from_date_to_date(currency, start_date, end_date):
    try:
        start_date_dt = datetime.strptime(start_date, format(DATE_FORMAT)).date()
        end_date_dt = datetime.strptime(end_date, format(DATE_FORMAT)).date()
        if start_date_dt > MAX_DATE or start_date_dt < MIN_DATE:
            return jsonify(cause="Start date out of the date range."), 400
        if end_date_dt > MAX_DATE or end_date_dt < MIN_DATE:
            return jsonify(cause="End date out of the date range."), 400
        if end_date_dt < start_date_dt:
            return jsonify(couse="End date before start date."), 400
    except ValueError:
        return jsonify(cause="Invalid date format."), 400

    return jsonify(sales=get_sale_in_USD_PLN_from_date_to_date(currency, start_date, end_date))


@app.teardown_appcontext
def close_database_connection(exception):
    close_connection(exception)

app.run()
