import flask
import threading
import cache
import constans as const
import db_handler as dbh
from flask import jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from data_verifiers import date_format_ok, db_contains_year, dates_order_ok, to_datetime
from datetime import timedelta

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[const.DEFAULT_DAY_LIMIT, const.DEFAULT_HOUR_LIMIT]
)


def period_validation(start_date, end_date):
    if not date_format_ok(start_date) or not date_format_ok(end_date):
        return jsonify(error='Invalid date format'), const.BAD_REQUEST

    if not db_contains_year(start_date) or not db_contains_year(end_date):
        return jsonify(error='Dates out of available range'), const.RANGE_NOT_SATISFIABLE

    if not dates_order_ok(start_date, end_date):
        return jsonify(error='Wrong dates order'), const.BAD_REQUEST

    return const.VALIDATION_OK


def date_validation(date):
    if not date_format_ok(date):
        return jsonify(error='Invalid date format'), const.BAD_REQUEST

    if not db_contains_year(date):
        return jsonify(error='There is no data for given year'), const.NOT_FOUND

    return const.VALIDATION_OK


@app.route('/api/rates/<date>', methods=['GET'])
def get_rate_for_date(date):
    validation_res = date_validation(date)
    if validation_res != const.VALIDATION_OK:
        return validation_res

    if date not in cache.rates:
        data = dbh.fetch_rate_for_date(date)
        if not data:
            return jsonify(error='There is no data for given date'), const.NOT_FOUND

        response = [{'date': date,
                     'rate': data[0][1],
                     'interpolated': data[0][2]}]

        cache.write_rate_to_cache(response[0])

        return jsonify(currency=const.CURRENCY, rates=response), const.OK

    response = [cache.rates[date]]

    return jsonify(currency=const.CURRENCY, rates=response), const.OK


@app.route('/api/rates/<start_date>/<end_date>', methods=['GET'])
def get_rates_for_period(start_date, end_date):
    validation_res = period_validation(start_date, end_date)
    if validation_res != const.VALIDATION_OK:
        return validation_res

    response = []

    if not cache.contains_period_rates((start_date, end_date)):
        data = dbh.fetch_rates_for_period((start_date, end_date))
        if not data:
            return jsonify(error='There is no data for given date'), const.NOT_FOUND

        for value in data:
            response.append({'date': value[0],
                             'rate': value[1],
                             'interpolated': value[2]})

        cache.write_period_rates(response, start_date, end_date)
        return jsonify(currency=const.CURRENCY, rates=response), const.OK

    current_date = to_datetime(start_date)
    end_date = to_datetime(end_date) + timedelta(days=1)
    while current_date != end_date:
        response.append(cache.rates[str(current_date)])
        current_date += timedelta(days=1)

    if not response:
        return jsonify(error='There is no data for given date'), const.NOT_FOUND

    return jsonify(currency=const.CURRENCY, rates=response), const.OK


@app.route('/api/sales/<date>', methods=['GET'])
def get_sales_for_date(date):
    validation_res = date_validation(date)
    if validation_res != const.VALIDATION_OK:
        return validation_res

    if date not in cache.sales:
        data = dbh.fetch_sale_and_rate_for_date(date)
        if not data:
            return jsonify(error='There is no data for given date'), const.NOT_FOUND

        response = [{'date': date,
                     'rate': data[0][1],
                     'usd_sale': data[0][2],
                     'pln_sale': float(data[0][1]) * float(data[0][2])}]

        cache.write_sale_to_cache(response[0])
        return jsonify(sale=response), const.OK

    response = [cache.sales[date]]

    return jsonify(sale=response), const.OK


@app.route('/api/sales/<start_date>/<end_date>', methods=['GET'])
def get_sales_for_period(start_date, end_date):
    validation_res = period_validation(start_date, end_date)
    if validation_res != const.VALIDATION_OK:
        return validation_res

    response = []

    if not cache.contains_period_sales((start_date, end_date)):
        data = dbh.fetch_sales_and_rates_for_period((start_date, end_date))
        if not data:
            return jsonify(error='There is no data for given date'), const.NOT_FOUND

        for value in data:
            response.append({'date': value[0],
                             'rate': value[1],
                             'usd_sale': value[2],
                             'pln_sale': float(value[1]) * float(value[2])})

        cache.write_period_sales(response, start_date, end_date)
        return jsonify(sale=response), const.OK

    start_date = to_datetime(start_date)
    end_date = to_datetime(end_date)
    keys = [k for k in cache.sales.keys() if start_date <= to_datetime(k) <= end_date]

    if not keys:
        return jsonify(error='There is no data for given date'), const.NOT_FOUND

    for key in keys:
        response.append(cache.sales[key])

    return jsonify(sale=response), const.OK


def run_api():
    if const.DEFAULT_CACHING:
        cache.update_rates()
        cache.update_sales()

    cache_daemon = threading.Thread(target=cache.updates_manager, args=(const.DEFAULT_CACHING, ), daemon=True)
    cache_daemon.start()
    app.run()


if __name__ == '__main__':
    run_api()
