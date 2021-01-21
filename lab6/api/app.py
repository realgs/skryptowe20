import datetime

import flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3

date_begin = datetime.datetime(2009, 1, 1)
date_end = datetime.datetime(2010, 12, 31)

app = flask.Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10/minute"]
)


def __execute_query(query):
    connection = sqlite3.connect('chinook.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


available_currencies = ['USD', 'PLN']


def __convert_exchange_rate(usd_rate, currency):
    if currency == 'USD':
        return usd_rate
    elif currency == 'PLN':
        return round(1 / usd_rate, 4)
    else:
        return 0


@app.route('/api/exchangerate/<string:currency>/<int:year>-<int:month>-<int:day>', methods=['GET'])
@app.route('/api/exchangerate/<string:currency>/<int:year>-<int:month>-<int:day>/', methods=['GET'])
def get_exchange_rate_of_day(currency, year, month, day):
    currency = currency.upper()
    if currency not in available_currencies:
        return "<h1>400: BadRequest. Unknown currency", 400

    date = datetime.datetime(year, month, day)
    if date < date_begin or date_end < date:
        return "<h1>400: BadRequest. Date out of range", 400

    formatted_date = date.strftime("%Y-%m-%d")
    query = "SELECT date, price, interpolated FROM exchange_rate WHERE date = \'{}\'".format(formatted_date)
    (date, rate_usd, interpolated) = __execute_query(query)[0]

    rate = __convert_exchange_rate(rate_usd, currency)

    return {'code': currency,
            'result': [{'day': date, 'rate': rate, 'interpolated': True if interpolated == 1 else False}]}


@app.route(
    '/api/exchangerate/<string:currency>/<int:year_from>-<int:month_from>-<int:day_from>/<int:year_to>-<int:month_to>-<int:day_to>',
    methods=['GET'])
@app.route(
    '/api/exchangerate/<string:currency>/<int:year_from>-<int:month_from>-<int:day_from>/<int:year_to>-<int:month_to>-<int:day_to>/',
    methods=['GET'])
def get_exchange_rate_of_range(currency, year_from, month_from, day_from, year_to, month_to, day_to):
    currency = currency.upper()
    if currency not in available_currencies:
        return "<h1>400: BadRequest. Unknown currency", 400

    date_from = datetime.datetime(year_from, month_from, day_from)
    date_to = datetime.datetime(year_to, month_to, day_to)

    if date_from < date_begin:
        date_from = date_begin
    if date_end < date_to:
        date_to = date_end

    if date_to < date_from:
        return "<h1>400: BadRequest. Wrong date range", 400

    formatted_date_from = date_from.strftime("%Y-%m-%d")
    formatted_date_to = date_to.strftime("%Y-%m-%d")

    query = "SELECT date, price, interpolated FROM exchange_rate WHERE date BETWEEN \'{}\' AND \'{}\'".format(
        formatted_date_from,
        formatted_date_to)
    query_result = __execute_query(query)
    result = []
    for (date, price, interpolated) in query_result:
        rate = __convert_exchange_rate(price, currency)
        result.append({'day': date, 'rate': rate, 'interpolated': True if interpolated == 1 else False})
    return {'code': currency, 'result': result}


@app.route('/api/sales/<int:year>-<int:month>-<int:day>', methods=['GET'])
@app.route('/api/sales/<int:year>-<int:month>-<int:day>/', methods=['GET'])
def get_sales_of_day(year, month, day):
    date = datetime.datetime(year, month, day)
    if date < date_begin or date_end < date:
        return "<h1>400: BadRequest. Date out of range", 400

    query = "SELECT date, sales_usd, sales_pln, number_of_sales FROM total_sales WHERE date = \'{}\'".format(
        date.strftime("%Y-%m-%d"))

    (date, sales_usd, sales_pln, number_of_sales) = __execute_query(query)[0]
    return {
        'result': [{'day': date, 'sales_usd': sales_usd, 'sales_pln': sales_pln, 'number_of_sales': number_of_sales}]}


@app.route(
    '/api/sales/<int:year_from>-<int:month_from>-<int:day_from>/<int:year_to>-<int:month_to>-<int:day_to>',
    methods=['GET'])
@app.route(
    '/api/sales/<int:year_from>-<int:month_from>-<int:day_from>/<int:year_to>-<int:month_to>-<int:day_to>/',
    methods=['GET'])
def get_sales_of_range(year_from, month_from, day_from, year_to, month_to, day_to):
    date_from = datetime.datetime(year_from, month_from, day_from)
    date_to = datetime.datetime(year_to, month_to, day_to)

    if date_from < date_begin:
        date_from = date_begin
    if date_end < date_to:
        date_to = date_end

    if date_to < date_from:
        return "<h1>400: BadRequest. Wrong date range", 400

    query = "SELECT date, sales_usd, sales_pln, number_of_sales FROM total_sales WHERE date BETWEEN \'{}\' AND \'{}\'".format(
        date_from.strftime("%Y-%m-%d"), date_to.strftime("%Y-%m-%d"))
    query_results = __execute_query(query)
    result = []
    for (date, sales_usd, sales_pln, number_of_sales) in query_results:
        result.append({'day': date, 'sales_usd': sales_usd, 'sales_pln': sales_pln, 'number_of_sales': number_of_sales})
    return {'result': result}


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404: PageNotFound</h1>", 404


@app.errorhandler(429)
def aaa(e):
    return "<h1>429: TooManyRequests. Limit: 10 per minute per user", 429


if __name__ == '__main__':
    app.run()
