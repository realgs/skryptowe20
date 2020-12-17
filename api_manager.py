import flask
import constans
import threading
from flask import jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from data_verifiers import date_format_ok, db_contains_year, dates_order_ok, to_datetime
from cache import rates_cache, sales_cache, updates_manager
from datetime import timedelta

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[constans.DEFAULT_DAY_LIMIT, constans.DEFAULT_HOUR_LIMIT]
)


def period_validation(start_date, end_date):
    if not date_format_ok(start_date) or not date_format_ok(end_date):
        return jsonify(error='Invalid date format'), constans.BAD_REQUEST

    if not db_contains_year(start_date) or not db_contains_year(end_date):
        return jsonify(error='Dates out of available range'), constans.RANGE_NOT_SATISFIABLE

    if not dates_order_ok(start_date, end_date):
        return jsonify(error='Wrong dates order'), constans.BAD_REQUEST

    return constans.VALIDATION_OK


def date_validation(date):
    if not date_format_ok(date):
        return jsonify(error='Invalid date format'), constans.BAD_REQUEST

    if not db_contains_year(date):
        return jsonify(error='There is no data for given year'), constans.NOT_FOUND

    return constans.VALIDATION_OK


@app.route('/api/rates/<date>', methods=['GET'])
def get_rate_for_date(date):
    validation_res = date_validation(date)
    if validation_res != constans.VALIDATION_OK:
        return validation_res

    response = [{'date': date,
                 'rate': rates_cache[date]['rate'],
                 'interpolated': rates_cache[date]['interpolated']}]

    return jsonify(currency=constans.CURRENCY, rates=response), constans.OK


@app.route('/api/rates/<start_date>/<end_date>', methods=['GET'])
def get_rates_for_period(start_date, end_date):
    validation_res = period_validation(start_date, end_date)
    if validation_res != constans.VALIDATION_OK:
        return validation_res

    response = []
    current_date = to_datetime(start_date)
    end_date = to_datetime(end_date) + timedelta(days=1)
    while current_date != end_date:
        response.append({'date': str(current_date),
                         'rate': rates_cache[str(current_date)]['rate'],
                         'interpolated': rates_cache[str(current_date)]['interpolated']})
        current_date += timedelta(days=1)

    return jsonify(currency=constans.CURRENCY, rates=response), constans.OK


@app.route('/api/sales/<date>', methods=['GET'])
def get_sales_for_date(date):
    validation_res = date_validation(date)
    if validation_res != constans.VALIDATION_OK:
        return validation_res

    response = [{'date': date,
                 'rate': sales_cache[date]['rate'],
                 'usd_sum': sales_cache[date]['usd_sum'],
                 'pln_sum': sales_cache[date]['pln_sum']}]

    return jsonify(sale=response), constans.OK


@app.route('/api/sales/<start_date>/<end_date>', methods=['GET'])
def get_sales_for_period(start_date, end_date):
    validation_res = period_validation(start_date, end_date)
    if validation_res != constans.VALIDATION_OK:
        return validation_res

    start_date = to_datetime(start_date)
    end_date = to_datetime(end_date)
    keys = [k for k in sales_cache.keys() if start_date <= to_datetime(k) <= end_date]
    response = []
    for key in keys:
        response.append({'date': key,
                         'rate': sales_cache[key]['rate'],
                         'usd_sum': sales_cache[key]['usd_sum'],
                         'pln_sum': sales_cache[key]['pln_sum']})

    return jsonify(sale=response), constans.OK


x = threading.Thread(target=updates_manager, daemon=True)
x.start()
app.run()
