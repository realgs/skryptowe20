import datetime

import flask
from flask import request, jsonify
import sqlite3

date_begin = datetime.datetime(2009, 1, 1)
date_end = datetime.datetime(2010, 12, 31)

app = flask.Flask(__name__)


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


@app.route('/api/<string:currency>/<int:year>-<int:month>-<int:day>', methods=['GET'])
@app.route('/api/<string:currency>/<int:year>-<int:month>-<int:day>/', methods=['GET'])
def get_exchange_rate_of_day(currency, year, month, day):
    currency = currency.upper()
    if currency not in available_currencies:
        return "<h1>400: BadRequest. Unknown currency"

    date = datetime.datetime(year, month, day)
    if date < date_begin or date_end < date:
        return "<h1>400: BadRequest. Date out of range"

    formatted_date = date.strftime("%Y-%m-%d")
    query = "SELECT * FROM exchange_rate WHERE date = \'{}\'".format(formatted_date)
    query_result = __execute_query(query)[0]

    rate = __convert_exchange_rate(query_result[1], currency)

    return {'code': currency, 'result': [{'day': query_result[0], 'rate': rate}]}


@app.route('/api/<string:currency>/<int:year_from>-<int:month_from>-<int:day_from>/<int:year_to>-<int:month_to>-<int:day_to>', methods=['GET'])
@app.route('/api/<string:currency>/<int:year_from>-<int:month_from>-<int:day_from>/<int:year_to>-<int:month_to>-<int:day_to>/', methods=['GET'])
def get_exchange_rate_of_range(currency, year_from, month_from, day_from, year_to, month_to, day_to):
    currency = currency.upper()
    if currency not in available_currencies:
        return "<h1>400: BadRequest. Unknown currency"

    date_from = datetime.datetime(year_from, month_from, day_from)
    date_to = datetime.datetime(year_to, month_to, day_to)

    if date_from < date_begin:
        date_from = date_begin
    if date_end < date_to:
        date_to = date_end

    if date_to < date_from:
        return "<h1>400: BadRequest. Wrong date range"

    formatted_date_from = date_from.strftime("%Y-%m-%d")
    formatted_date_to = date_to.strftime("%Y-%m-%d")

    query = "SELECT * FROM exchange_rate WHERE date BETWEEN \'{}\' AND \'{}\'".format(formatted_date_from,
                                                                                      formatted_date_to)
    query_result = __execute_query(query)
    result = []
    for (date, price) in query_result:
        rate = __convert_exchange_rate(price, currency)
        result.append({'day': date, 'rate': rate})
    return {'code': 'USD', 'result': result}


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404: PageNotFound</h1>"


if __name__ == '__main__':
    app.run()
