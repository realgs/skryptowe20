import flask
from flask import jsonify
import constans
from data_verifiers import date_format_ok, db_contains_year, dates_order_ok, to_datetime
from cache import rates
from datetime import timedelta

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/rates/<date>', methods=['GET'])
def get_rate_for_date(date):
    if not date_format_ok(date):
        return jsonify(error='Invalid date format'), constans.BAD_REQUEST

    if not db_contains_year(date):
        return jsonify(error='There is no data for given year'), constans.NOT_FOUND

    response = [{'date': date,
                 'interpolated': rates[date]['interpolated'],
                 'rate': rates[date]['rate']}]

    return jsonify(currency=constans.CURRENCY, rates=response), constans.OK


@app.route('/api/rates/<start_date>/<end_date>', methods=['GET'])
def get_rates_for_period(start_date, end_date):
    if not date_format_ok(start_date) or not date_format_ok(end_date):
        return jsonify(error='Invalid date format'), constans.BAD_REQUEST

    if not db_contains_year(start_date) or not db_contains_year(end_date):
        return jsonify(error='Dates out of available range'), constans.RANGE_NOT_SATISFIABLE

    if not dates_order_ok(start_date, end_date):
        return jsonify(error='Wrong dates order'), constans.BAD_REQUEST

    response = []
    current_date = to_datetime(start_date)
    end_date = to_datetime(end_date) + timedelta(days=1)
    while current_date != end_date:
        response.append({'date': str(current_date),
                         'interpolated': rates[str(current_date)]['interpolated'],
                         'rate': rates[str(current_date)]['rate']})
        current_date += timedelta(days=1)

    return jsonify(currency=constans.CURRENCY, rates=response), constans.OK


app.run()
