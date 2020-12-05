import flask
import sqlite3
from flask import request, jsonify
from quoteDataObject import QuoteDataObject
from sales import Sales


def startAPI():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    databaseFile = 'sales_data_base.db'
    sales = Sales()

    @app.route('/', methods=['GET'])
    def home():
        return '''<h1>My sales api</h1>
             <p>Damian Żółtowski 246651</p>'''


    @app.route('/api/rates/fordate', methods=['GET'])
    def getRateForDay():
        connection = sqlite3.connect(databaseFile)
        cursor = connection.cursor()
        if 'date' in request.args:
            requestedDate = str(request.args['date'])
        else:
            return 'ERROR: You need to specify date to get the exchange rate', 401
        cursor.execute('SELECT * FROM CurrencyQuotes WHERE date = (?)', (requestedDate,))
        result = cursor.fetchone()
        connection.close()
        if result is None:
            return 'ERROR: No data found for specified date', 501
        result = QuoteDataObject(result[0], result[1], bool(result[2]))
        return jsonify(result), 200

    @app.route('/api/rates/fordatespan', methods=['GET'])
    def getRateForDateSpan():
        connection = sqlite3.connect(databaseFile)
        cursor = connection.cursor()
        if 'from' not in request.args:
            return 'ERROR: You need to specify date from which you want the results', 401
        elif 'to' not in request.args :
            return 'ERROR: You need to specify date to which you want the results', 401
        else:
            dateFrom = str(request.args['from'])
            dateTo = str(request.args['to'])
        cursor.execute(f'SELECT * FROM CurrencyQuotes WHERE date <= (?) AND date >= (?) ORDER BY date DESC', (dateFrom, dateTo))
        result = cursor.fetchall()
        connection.close()
        if result is None:
            return 'ERROR: No data could be found for specified date span', 501
        quotes = []
        for element in result:
            quotes.append(QuoteDataObject(element[0], element[1], bool(element[2])))
        return jsonify(quotes), 200

    @app.route('/api/sales/forday', methods=['GET'])
    def getSalesForDay():
        nonlocal sales                  # Jako zmienna nielokalna jest ona inicjalizowana tylko na początku
        if not sales.salesArray:        # odpalenia API, potem wartości są zaciągane z klasy, która przechowuje
            sales.calculateSales()      # te wartości
        if 'date' in request.args:
            requestedDate = str(request.args['date'])
        else:
            return 'ERROR: You need to specify date to get the exchange rate', 401
        result = sales.findSales(requestedDate)
        if result is None:
            return 'ERROR: No data could be found for given date', 501
        return jsonify(result), 200

    app.run()
