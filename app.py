import flask
import sqlite3
import datetime
from flask import abort, request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def get_string_date_from_date(date):
    try:
        selected_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        string_date = selected_date.strftime("%Y-%m-%d")
        return string_date
    except ValueError:
        return ""


def get_result_from_query(query, parameter):
    connection = sqlite3.connect("Northwind.sqlite")
    cursor = connection.cursor()

    cursor.execute(query, parameter)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/api/exchangerates/<date>', methods=['GET'])
def api_single_exchange_rate(date):
    string_date = get_string_date_from_date(date)
    if "" == string_date:
        abort(404, "Wrong date format")

    select_single_exchange_rate_query = """SELECT ER.date, ER.rate, ER.is_interpolated FROM ExchangeRate ER 
    WHERE ER.date = ?;"""
    result = get_result_from_query(select_single_exchange_rate_query, (string_date,))

    return jsonify(result)


@app.route('/api/exchangerates/<start_date>/<end_date>', methods=['GET'])
def api_exchange_rate_range(start_date, end_date):
    string_start_date = get_string_date_from_date(start_date)
    string_end_date = get_string_date_from_date(end_date)

    if string_start_date == "" or string_end_date == "" or string_end_date < string_start_date:
        abort(404, "Wrong dates provided")

    select_multiple_exchange_rates_query = """SELECT ER.date, ER.rate, ER.is_interpolated FROM ExchangeRate ER 
    WHERE ER.date >= ? AND ER.DATE <= ?;"""

    result = get_result_from_query(select_multiple_exchange_rates_query, (string_start_date, string_end_date))

    return jsonify(result)


@app.route('/api/sum/<currency>/<date>', methods=['GET'])
def api_single_sum_of_transaction(currency, date):
    string_date = get_string_date_from_date(date)

    if "" == string_date:
        abort(404, "Wrong date format")

    currency = currency.upper()

    select_single_exchange_rate_query = ""

    if currency == "PLN":
        select_single_exchange_rate_query = """SELECT ST.date, ST.pln_value FROM SumOfTransaction ST 
        WHERE ST.date = ?;"""
    elif currency == "USD":
        select_single_exchange_rate_query = """SELECT ST.date, ST.usd_value FROM SumOfTransaction ST 
                WHERE ST.date = ?;"""
    else:
        abort(404, "Wrong currency")

    result = get_result_from_query(select_single_exchange_rate_query, (string_date,))

    return jsonify(result)


if __name__ == "__main__":
    app.run()
