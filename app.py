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

    cursor.execute(query, (parameter,))
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/api/exchangerates/<date>', methods=['GET'])
def api_single_exchange_rate(date):
    string_date = get_string_date_from_date(date)
    if "" == string_date:
        abort(404, "Wrong date format")

    select_single_exchange_rate_query = """SELECT ER.date, ER.rate FROM ExchangeRate ER WHERE ER.date = ?;"""
    result = get_result_from_query(select_single_exchange_rate_query, string_date)

    return jsonify(result)


if __name__ == "__main__":
    app.run()
