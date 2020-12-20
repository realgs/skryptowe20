import flask
import sqlite3
import datetime
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/exchangerates/<date>', methods=['GET'])
def api_single_exchange_rate(date):
    try:
        selected_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        string_date = selected_date.strftime("%Y-%m-%d")
    except ValueError:
        return jsonify([])

    connection = sqlite3.connect("Northwind.sqlite")
    cursor = connection.cursor()

    select_single_exchange_rate = """SELECT ER.date, ER.rate FROM ExchangeRate ER WHERE ER.date = ?;"""

    cursor.execute(select_single_exchange_rate, (string_date,))
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return jsonify(result)


if __name__ == "__main__":
    app.run()
