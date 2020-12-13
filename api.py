from datetime import timedelta, datetime, date
import flask
import database
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import requests
from flask import jsonify, abort

API_LIMIT = 366
STATUS_OK = 200

BAD_REQUEST = 400
WRONG_DATE_RANGE = 416
NO_DATA_FOUND = 404


def getSalesRate(saleDatetime):
    date_format = saleDatetime.strftime("%Y-%m-%d")

    sale = database.getSaleFromDatabase(saleDatetime)
    rate = getUSDCorrectRate(saleDatetime)
    result = {}
    if type(sale) == int:
        abort(sale)
    if date_format in sale.keys() and date_format in rate.keys():
        result[date_format] = {}
        result[date_format]["USD"] = sale[date_format]
        result[date_format]["PLN"] = sale[date_format] * rate[date_format]["rate"]
    return result


def getSalesRates(startDatetime, endDatetime):
    sales = database.getSalesFromDatabase(startDatetime, endDatetime)
    rates = getCorrectedUsdRates(startDatetime, endDatetime)
    if type(sales) == int:
        abort(sales)
    result = {}
    for data in sales.keys():
        result[data] = {}
        result[data]["USD"] = sales[data]
        result[data]["PLN"] = sales[data] * rates[data]["rate"]
    return result


def getCorrectedUsdRates(startDatetime, endDatetime):
    if startDatetime == endDatetime:
        return getUSDCorrectRate(startDatetime)
    rates_from_server = getUsdRates(startDatetime, endDatetime)
    correct_rates = {}
    delta = endDatetime - startDatetime
    for i in range(delta.days + 1):
        actual_datetime = startDatetime + timedelta(days=i)
        correct_rates[actual_datetime.strftime('%Y-%m-%d')] = getCorrectRate(rates_from_server, actual_datetime)
    return correct_rates


def getUSDCorrectRate(rateDatetime):
    current_date = rateDatetime
    date_format = rateDatetime.strftime("%Y-%m-%d")
    return_date_format = date_format

    result = {}
    while len(result.keys()) == 0:
        resp = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/A/USD/{date_format}/")
        if resp.status_code == STATUS_OK:
            result[return_date_format] = {}
            result[return_date_format]["rate"] = resp.json()['rates'][0]['mid']
            if current_date != rateDatetime:
                result[return_date_format]["interpolated"] = "true"
            else:
                result[return_date_format]["interpolated"] = "false"
        else:
            current_date -= timedelta(days=1)
            date_format = current_date.strftime("%Y-%m-%d")
    return result


def getUsdRates(startDatetime, endDatetime):
    start_date = startDatetime
    end_date = endDatetime
    start_date_format = start_date.strftime('%Y-%m-%d')
    end_date_format = end_date.strftime('%Y-%m-%d')
    rates = {}
    while start_date != end_date:
        if start_date < end_date - timedelta(days=API_LIMIT):
            resp = requests.get(
                f"http://api.nbp.pl/api/exchangerates/rates/A/USD/{start_date_format}/{(start_date + timedelta(days=API_LIMIT)).strftime('%Y-%m-%d')}/")
            if resp.status_code == STATUS_OK:
                for rate in resp.json()['rates']:
                    if "first_date" not in rates.keys():
                        rates["first_date"] = rate['effectiveDate']
                    rates[rate['effectiveDate']] = rate['mid']
            start_date = start_date + timedelta(days=(API_LIMIT + 1))
            start_date_format = start_date.strftime('%Y-%m-%d')
        else:
            resp = requests.get(
                f"http://api.nbp.pl/api/exchangerates/rates/A/USD/{start_date_format}/{end_date_format}/")
            if resp.status_code == STATUS_OK:
                for rate in resp.json()['rates']:
                    if "first_date" not in rates.keys():
                        rates["first_date"] = rate['effectiveDate']
                    rates[rate['effectiveDate']] = rate['mid']
            start_date = end_date
            start_date_format = start_date.strftime('%Y-%m-%d')
    return rates


def getCorrectRate(rates, rateDatetime):
    checking_date = rateDatetime
    checking_date_format = checking_date.strftime('%Y-%m-%d')
    result = {}
    if checking_date < datetime.strptime(rates["first_date"], "%Y-%m-%d"):
        correct_rate = getUSDCorrectRate(checking_date)
        result["rate"] = correct_rate[checking_date_format]["rate"]
        result["interpolated"] = correct_rate[checking_date_format["interpolated"]]
        return result
    if checking_date_format in rates.keys():
        result["rate"] = rates[checking_date_format]
        result["interpolated"] = "false"
        return result
    while checking_date_format not in rates.keys():
        checking_date -= timedelta(days=1)
        checking_date_format = checking_date.strftime('%Y-%m-%d')
    result["rate"] = rates[checking_date_format]
    result["interpolated"] = "true"
    return result


def datetimeSingleDateCheck(dateToCheck):
    try:
        date_datetime = datetime.strptime(dateToCheck, "%Y-%m-%d")
    except:
        abort(400, description="Wrong date format, it should be like 2020-07-12")

    if date_datetime >= datetime.strptime(str(date.today()), "%Y-%m-%d"):
        abort(416,
              description="Wrong date range, date should be less than today's date")
    return date_datetime


def datetimeDoubleDateCheck(dateToCheck1, dateToCheck2):
    try:
        start_datetime = datetime.strptime(dateToCheck1, "%Y-%m-%d")
        end_datetime = datetime.strptime(dateToCheck2, "%Y-%m-%d")
    except:
        abort(400, description="Wrong date format, it should be like 2020-07-12")

    if start_datetime > end_datetime or end_datetime >= datetime.strptime(str(date.today()), "%Y-%m-%d"):
        abort(416,
              description="Wrong date range, the last date should be greater than the first date and the last date "
                          "should be less than today's date")
    return start_datetime, end_datetime


app = flask.Flask(__name__)
app.config["DEBUG"] = True

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['200 per day', '50 per hour']
)

app_limit = limiter.shared_limit("200 per minute", scope="API")


@app.route('/', methods=['GET'])
def home():
    return f'''<h1>API - Lista 5</h1>
<p>Michał Chrobot 246665</p>'''


@app.route('/USD/<ratingDate>', methods=['GET'])
@limiter.limit('60 per minute')
@app_limit
def api_date(ratingDate):
    date_datetime = datetimeSingleDateCheck(ratingDate)
    return jsonify(getUSDCorrectRate(date_datetime))


@app.route('/USD/<dateFrom>/<dateTo>', methods=['GET'])
@limiter.limit('10 per minute')
@app_limit
def api_date_from_to(dateFrom, dateTo):
    start_datetime, end_datetime = datetimeDoubleDateCheck(dateFrom, dateTo)
    return jsonify(getCorrectedUsdRates(start_datetime, end_datetime))


@app.route('/sales/<ratingDate>', methods=['GET'])
@limiter.limit('60 per minute')
@app_limit
def api_sale(ratingDate):
    date_datetime = datetimeSingleDateCheck(ratingDate)
    return jsonify(getSalesRate(date_datetime))


@app.route('/sales/<dateFrom>/<dateTo>', methods=['GET'])
@limiter.limit('10 per minute')
@app_limit
def api_sales_from_to(dateFrom, dateTo):
    start_datetime, end_datetime = datetimeDoubleDateCheck(dateFrom, dateTo)
    return jsonify(getSalesRates(start_datetime, end_datetime))


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(416)
def wrong_range(e):
    return jsonify(error=str(e)), 416


app.run()
