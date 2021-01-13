import flask
import sqlite3
import time
from flask import request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
from quoteDataObject import QuoteDataObject
from sales import Sales



app = flask.Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
databaseFile = 'sales_data_base.db'
sales = Sales()
limiter = Limiter(app, key_func=get_remote_address, default_limits=['300 per day'])
timeStart = time.time()

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return '''<h1>My sales api</h1>
         <p>Damian Żółtowski 246651</p>'''


@app.route('/api/rates/fordate', methods=['GET'])
@limiter.limit('15 per minute')
@limiter.limit('100 per hour')
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
@limiter.limit('5 per minute')
@limiter.limit('70 per hour')
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
    cursor.execute(f'SELECT * FROM CurrencyQuotes WHERE date >= (?) AND date <= (?) ORDER BY date DESC', (dateFrom, dateTo))
    result = cursor.fetchall()
    connection.close()
    if result is None or result == []:
        return 'ERROR: No data could be found for specified date span', 501
    quotes = []
    for element in result:
        quotes.append(QuoteDataObject(element[0], element[1], bool(element[2])))
    return jsonify(quotes), 200

@app.route('/api/sales/fordate', methods=['GET'])
@limiter.limit('10 per minute')
@limiter.limit('90 per hour')
def getSalesForDay():
    salesLocal = sales                                              # Jako zmienna nielokalna jest ona inicjalizowana tylko na początku
    timeDiff = time.time() - timeStart                              # odpalenia API. Po skopiowaniu referencji do zmiennej lokalnej salesLocal,
    if not salesLocal.salesArray or int(timeDiff) / 57600 >= 1:     # wartości sprzedaży są zaciągane z klasy sales, która przechowuje je
        salesLocal.calculateSales()                                 # w postaci obiektów salesDataObject.
    if 'date' in request.args:                                      # a zmienna timeDiff odświeża bazę danych co 58 600 sekund czyli 16h
        requestedDate = str(request.args['date'])
    else:
        return 'ERROR: You need to specify date to get the exchange rate', 401
    result = salesLocal.findSales(requestedDate)
    if result is None:
        return 'ERROR: No data could be found for given date', 501
    return jsonify(result), 200

@app.route('/api/sales/fordatespan', methods=['GET'])
@limiter.limit('5 per minute')
@limiter.limit('60 per hour')
def getSalesForDateSpan():
    salesLocal = sales
    timeDiff = time.time() - timeStart
    if not salesLocal.salesArray or int(timeDiff) / 57600 >= 1:
        salesLocal.calculateSales()
    if 'from' not in request.args:
        return 'ERROR: You need to specify date from which you want the results', 401
    elif 'to' not in request.args:
        return 'ERROR: You need to specify date to which you want the results', 401
    else:
        dateFrom = str(request.args['from'])
        dateTo = str(request.args['to'])
    result = salesLocal.findSalesForDates(dateFrom, dateTo)
    if result is None or result == []:
        return 'ERROR: No data could be found for given date', 501
    return jsonify(result), 200

app.run()
