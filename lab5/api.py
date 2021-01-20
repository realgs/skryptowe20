import flask
from flask import render_template, request, json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta

import db

DATABASE = r"C:\Users\Patrycja\Desktop\5 semestr\Języki skryptowe\salesData.db"
MINDATE = '2013-01-04'
MAXDATE = '2016-12-29'
CURRENCIES = ["USD", "PLN"]
DATA_TYPES = ["Rates", "Sales"]
SALES_LAST_CACHED = datetime.now()

app = flask.Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,  # limit na osobe po ip
    default_limits=["300 per day", "20 per minute"],
    application_limits=["10000 per day", "300 per minute", "10 per second"]  # limit na cala aplikacje
)
app.config["DEBUG"] = True
SALES = []


@app.route('/', methods=['GET'])
def home():
    return render_template("main-page.html")


@app.route('/select', methods=['GET'])
def select_gui():
    context = {'min_date': MINDATE, 'max_date': MAXDATE, 'currencies': CURRENCIES,
               'data_types': DATA_TYPES}
    return render_template("select-page.html", data=context)


@app.route('/select/data', methods=['get'])
def return_data():
    args = request.args
    data_type = args['dataType']
    currency = args['currency']
    start_date = args['startDate']
    end_date = args['endDate']
    missing_data, result_data = process_data(data_type, currency, start_date, end_date)
    if data_type == 'Rates':
        if len(end_date) != 0 and not missing_data:
            chart_data = get_rates_chart_data(result_data)
            return render_template("rates-page.html", missing_data=missing_data, currency=currency, data=result_data,
                                   chart_data=chart_data)
        return render_template("rates-page.html", missing_data=missing_data, currency=currency, data=result_data)
    else:
        if len(end_date) != 0 and not missing_data:
            chart_data = get_sales_chart_data(result_data, currency, start_date, end_date)
            return render_template("sales-page.html", missing_data=missing_data, currency=currency, data=result_data,
                                   chart_data=chart_data)
        return render_template("sales-page.html", missing_data=missing_data, currency=currency, data=result_data)


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
    return json.dumps(result)


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
    return json.dumps(result)


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
    return json.dumps(result)


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
    return json.dumps(result)


@app.route('/api/sales/<date>', methods=['GET'])
def api_sales(date):
    global SALES_LAST_CACHED
    if date < MINDATE or date > MAXDATE:
        return 'ERROR: Given date is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    if len(SALES) == 0 or SALES_LAST_CACHED <= datetime.now() - timedelta(hours=24):
        SALES.clear()
        print('Fetching sales data...')
        conn = db.create_connection()
        with conn:
            allsales = db.get_all_sales(conn)
            for elem in allsales:
                elem['SalesPLN'] = elem['Sales'] * elem['RateValue']
                SALES.append(elem)
        SALES_LAST_CACHED = datetime.now()
    result = []
    for elem in SALES:
        if elem['Date'] == date:
            result.append(elem)
    if len(result) == 0:
        return 'ERROR: No data found. Sales on given day totalled 0'
    return json.dumps(result)


@app.route('/api/sales/<startdate>/<enddate>', methods=['GET'])
def api_sales_timespan(startdate, enddate):
    global SALES_LAST_CACHED
    if startdate > enddate:
        return 'ERROR: Invalid dates'
    if (startdate < MINDATE and enddate < MINDATE) or (startdate > MAXDATE and enddate > MAXDATE):
        return 'ERROR: Given time span is outside of supported range. ' \
               'Supported dates are from {} to {}'.format(MINDATE, MAXDATE)
    if startdate < MINDATE:
        startdate = MINDATE
    if enddate > MAXDATE:
        enddate = MAXDATE
    if len(SALES) == 0 or SALES_LAST_CACHED <= datetime.now() - timedelta(hours=24):
        SALES.clear()
        print('Fetching sales data...')
        conn = db.create_connection()
        with conn:
            allsales = db.get_all_sales(conn)
            for elem in allsales:
                elem['SalesPLN'] = elem['Sales'] * elem['RateValue']
                SALES.append(elem)
        SALES_LAST_CACHED = datetime.now()
    result = []
    for elem in SALES:
        if startdate <= elem['Date'] <= enddate:
            result.append(elem)
    if len(result) == 0:
        return 'ERROR: No data found. Sales on given days totalled 0'
    return json.dumps(result)


def process_data(data_type, currency, start_date, end_date):
    missing_data = False
    if data_type == 'Rates':
        if len(end_date) == 0:
            if currency == 'USD':
                temp_result = api_rates_usd_date(start_date)
            else:
                temp_result = api_rates_pln_date(start_date)
        else:
            if currency == 'USD':
                temp_result = api_rates_usd_timespan(start_date, end_date)
            else:
                temp_result = api_rates_pln_timespan(start_date, end_date)
        if temp_result.find("ERROR") != -1:
            result_data = []
            missing_data = True
        else:
            result_data = json.loads(temp_result)
    else:
        if len(end_date) == 0:
            temp_result = api_sales(start_date)
        else:
            temp_result = api_sales_timespan(start_date, end_date)
        if temp_result.find("ERROR") != -1:
            result_data = []
            missing_data = True
        else:
            result_data = json.loads(temp_result)
    return missing_data, result_data


def get_rates_chart_data(result_data):
    dates = []
    values = []
    for item in result_data:
        dates.append(item["Date"])
        values.append(item["Value"])
    return dates, values


def get_sales_chart_data(result_data, currency, start_date, end_date):
    dates = []
    values = []
    temp_data = {}
    sdate = datetime.strptime(start_date, '%Y-%m-%d')
    edate = datetime.strptime(end_date, '%Y-%m-%d')
    delta = edate - sdate
    for i in range(delta.days + 1):
        dates.append(datetime.strftime(sdate + timedelta(days=i), '%Y-%m-%d'))

    for item in result_data:
        if currency == 'USD':
            temp_data[item["Date"]] = item["Sales"]
        else:
            temp_data[item["Date"]] = item["SalesPLN"]

    for singe_date in dates:
        temp_val = temp_data.get(singe_date)
        if temp_val is None:
            values.append(0)
        else:
            values.append(temp_val)
    return dates, values


app.run()
