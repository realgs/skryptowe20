import flask
from flask import jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import db

DATABASE = r"C:\Users\Patrycja\Desktop\5 semestr\Języki skryptowe\salesData.db"
MINDATE = '2013-01-04'
MAXDATE = '2016-12-29'

app = flask.Flask(__name__)
# limit na osobe po ip
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["300 per day", "20 per minute"],
    application_limits=["10000 per day", "300 per minute", "10 per second"]
)
app.config["DEBUG"] = True
SALES = []


@app.route('/', methods=['GET'])
def home():
    return "<h1>Lab 5</h1>" \
           "<p>This site is an API for getting historical currency ratings from NBP API " \
           "completed with data for missing ratings. You can also access total sales data from my database</p>"


@app.route('/api/rates/USD/<date>', methods=['GET'])
def api_rates_usd_date(date):
    if date < MINDATE or date > MAXDATE:
        return 'ERROR: Given date is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    conn = db.create_connection()
    with conn:
        result = db.get_rate(conn, date)
    if len(result) == 0:
        return 'ERROR: No data found'
    return jsonify(result)


@app.route('/api/rates/PLN/<date>', methods=['GET'])
def api_rates_pln_date(date):
    if date < MINDATE or date > MAXDATE:
        return 'ERROR: Given date is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    conn = db.create_connection()
    with conn:
        result = db.get_rate(conn, date)
    for elem in result:
        val = 1 / elem['Value']
        elem['Value'] = val
    if len(result) == 0:
        return 'ERROR: No data found'
    return jsonify(result)


@app.route('/api/rates/USD/<startdate>/<enddate>', methods=['GET'])
def api_rates_usd_timespan(startdate, enddate):
    if startdate > enddate:
        return 'ERROR: Invalid dates'
    if (startdate < MINDATE and enddate < MINDATE) or (startdate > MAXDATE and enddate > MAXDATE):
        return 'ERROR: Given time span is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    if startdate < MINDATE:
        startdate = MINDATE
    if enddate > MAXDATE:
        enddate = MAXDATE
    conn = db.create_connection()
    with conn:
        result = db.get_multiple_rates(conn, startdate, enddate)
    return jsonify(result)


@app.route('/api/rates/PLN/<startdate>/<enddate>', methods=['GET'])
def api_rates_pln_timespan(startdate, enddate):
    if startdate > enddate:
        return 'ERROR: Invalid dates'
    if (startdate < MINDATE and enddate < MINDATE) or (startdate > MAXDATE and enddate > MAXDATE):
        return 'ERROR: Given time span is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    if startdate < MINDATE:
        startdate = MINDATE
    if enddate > MAXDATE:
        enddate = MAXDATE
    conn = db.create_connection()
    with conn:
        result = db.get_multiple_rates(conn, startdate, enddate)
    for elem in result:
        val = 1 / elem['Value']
        elem['Value'] = val
    return jsonify(result)


@app.route('/api/sales/<date>', methods=['GET'])
def api_sales(date):
    if date < MINDATE or date > MAXDATE:
        return 'ERROR: Given date is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    if len(SALES) == 0:
        print('Fetching sales data...')
        conn = db.create_connection()
        with conn:
            allsales = db.get_all_sales(conn)
            for elem in allsales:
                elem['SalesPLN'] = elem['Sales'] * elem['RateValue']
                SALES.append(elem)
    result = []
    for elem in SALES:
        if elem['Date'] == date:
            result.append(elem)
    if len(result) == 0:
        return 'ERROR: No data found. Sales on given day totalled 0'
    return jsonify(result)


@app.route('/api/sales/<startdate>/<enddate>', methods=['GET'])
def api_sales_timespan(startdate, enddate):
    if startdate > enddate:
        return 'ERROR: Invalid dates'
    if (startdate < MINDATE and enddate < MINDATE) or (startdate > MAXDATE and enddate > MAXDATE):
        return 'ERROR: Given time span is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    if startdate < MINDATE:
        startdate = MINDATE
    if enddate > MAXDATE:
        enddate = MAXDATE
    if len(SALES) == 0:
        print('Fetching sales data...')
        conn = db.create_connection()
        with conn:
            allsales = db.get_all_sales(conn)
            for elem in allsales:
                elem['SalesPLN'] = elem['Sales'] * elem['RateValue']
                SALES.append(elem)
    result = []
    for elem in SALES:
        if startdate <= elem['Date'] <= enddate:
            result.append(elem)
    if len(result) == 0:
        return 'ERROR: No data found. Sales on given days totalled 0'
    return jsonify(result)


app.run()
