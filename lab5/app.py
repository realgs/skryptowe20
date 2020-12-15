import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)


def __format_number(number):
    return str(number).rjust(2, '0')


def __format_date(year, month, day):
    return "{}-{}-{}".format(year, __format_number(month), __format_number(day))


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
        return 1 / usd_rate
    else:
        return 0


@app.route('/api/<string:currency>/<int:year>-<int:month>-<int:day>', methods=['GET'])
def get_exchange_rate_of_day(currency, year, month, day):
    currency = currency.upper()
    if currency not in available_currencies:
        raise Exception()

    formatted_date = __format_date(year, month, day)
    query = "SELECT * FROM exchange_rate WHERE date = \'{}\'".format(formatted_date)
    query_result = __execute_query(query)[0]

    rate = __convert_exchange_rate(query_result[1], currency)

    return {'code': currency, 'result': [{'day': query_result[0], 'rate': rate}]}


@app.route('/api/<string:currency>>/<int:year_from>-<int:month_from>-<int:day_from>/<int:year_to>-<int:month_to>-<int'
           ':day_to>', methods=['GET'])
def get_exchange_rate_of_range(currency, year_from, month_from, day_from, year_to, month_to, day_to):
    currency = currency.upper()
    if currency not in available_currencies:
        raise Exception()

    formatted_date_from = __format_date(year_from, month_from, day_from)
    formatted_date_to = __format_date(year_to, month_to, day_to)

    query = "SELECT * FROM exchange_rate WHERE date BETWEEN \'{}\' AND \'{}\'".format(formatted_date_from,
                                                                                      formatted_date_to)
    query_result = __execute_query(query)
    result = []
    for (date, price) in query_result:
        rate = __convert_exchange_rate(price, currency)
        result.append({'day': date, 'rate': rate})
    return {'code': 'USD', 'result': result}


if __name__ == '__main__':
    app.run()
