from datetime import timedelta, datetime, date
import flask
import database
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from cache import Cache

import requests
from flask import jsonify, abort, render_template

NBP_USD_REQUEST = "http://api.nbp.pl/api/exchangerates/rates/A/USD"

API_LIMIT = 366
STATUS_OK = 200

BAD_REQUEST = 400
WRONG_DATE_RANGE = 416
NO_DATA_FOUND = 404


def getSalesRate(saleDatetime):
    date_format = saleDatetime.strftime("%Y-%m-%d")

    sale = database.getSaleFromDatabase(saleDatetime)
    rate = getCorrectUSDRate(saleDatetime)
    result = {}
    if type(sale) == int:
        abort(sale)
    sumUSD = 0
    sumPLN = 0
    if date_format in sale.keys() and date_format in rate.keys():
        result[date_format] = {"USD": sale[date_format], "PLN": sale[date_format] * rate[date_format]["rate"]}
        cache.day_sales[date_format] = result[date_format]
        sumUSD += sale[date_format]
        sumPLN += sale[date_format] * rate[date_format]["rate"]
    result["sumPLN"] = sumPLN
    result["sumUSD"] = sumUSD
    return result


def getSalesRates(startDatetime, endDatetime):
    sales = database.getSalesFromDatabase(startDatetime, endDatetime)
    rates = getCorrectUSDRates(startDatetime, endDatetime)
    if type(sales) == int:
        abort(sales)
    result = {}
    sumUSD = 0
    sumPLN = 0
    for data in sales.keys():
        result[data] = {"USD": sales[data], "PLN": sales[data] * rates[data]["rate"]}
        cache.day_sales[data] = result[data]
        sumUSD += sales[data]
        sumPLN += sales[data] * rates[data]["rate"]
    result["sumPLN"] = sumPLN
    result["sumUSD"] = sumUSD
    return result


def getCorrectUSDRatesHelper(rates, rateDatetime):
    checking_date = rateDatetime
    checking_date_format = checking_date.strftime('%Y-%m-%d')
    result = {}
    if checking_date < datetime.strptime(rates["first_date"], "%Y-%m-%d"):
        correct_rate = getCorrectUSDRate(checking_date)
        result["rate"] = correct_rate[checking_date_format]["rate"]
        result["interpolated"] = correct_rate[checking_date_format]["interpolated"]
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


def getCorrectUSDRates(startDatetime, endDatetime):
    if startDatetime == endDatetime:
        return getCorrectUSDRate(startDatetime)
    rates_from_server = getUsdRates(startDatetime, endDatetime)
    correct_rates = {}
    delta = endDatetime - startDatetime
    for i in range(delta.days + 1):
        actual_datetime = startDatetime + timedelta(days=i)
        correct_rates[actual_datetime.strftime('%Y-%m-%d')] = getCorrectUSDRatesHelper(rates_from_server, actual_datetime)
        cache.day_rates[actual_datetime.strftime('%Y-%m-%d')] = correct_rates[actual_datetime.strftime('%Y-%m-%d')]
    return correct_rates


def getCorrectUSDRate(rateDatetime):
    current_date = rateDatetime
    date_format = rateDatetime.strftime("%Y-%m-%d")
    return_date_format = date_format

    result = {}
    while len(result.keys()) == 0:
        resp = requests.get(f"{NBP_USD_REQUEST}/{date_format}/")
        if resp.status_code == STATUS_OK:
            if current_date != rateDatetime:
                result[return_date_format] = {"rate": resp.json()['rates'][0]['mid'], "interpolated": "true"}
                cache.day_rates[return_date_format] = result[return_date_format]
            else:
                result[return_date_format] = {"rate": resp.json()['rates'][0]['mid'], "interpolated": "false"}
                cache.day_rates[return_date_format] = result[return_date_format]
        else:
            current_date -= timedelta(days=1)
            date_format = current_date.strftime("%Y-%m-%d")
    return result


def getUsdRatesHelper(start_date, start_date_format, end_date_format, rates):
    resp = requests.get(
        f"{NBP_USD_REQUEST}/{start_date_format}/{end_date_format}/")
    if resp.status_code == STATUS_OK:
        for rate in resp.json()['rates']:
            if "first_date" not in rates.keys():
                rates["first_date"] = rate['effectiveDate']
            rates[rate['effectiveDate']] = rate['mid']
    return start_date + timedelta(days=(API_LIMIT + 1)), start_date.strftime('%Y-%m-%d'), rates


def getUsdRates(startDatetime, endDatetime):
    start_date = startDatetime
    end_date = endDatetime
    start_date_format = start_date.strftime('%Y-%m-%d')
    end_date_format = end_date.strftime('%Y-%m-%d')
    rates = {}
    while start_date < end_date:
        if start_date < end_date - timedelta(days=API_LIMIT):
            start_date, start_date_format, rates = getUsdRatesHelper(start_date, start_date_format,
                                                                     (start_date + timedelta(days=API_LIMIT)).strftime(
                                                                         '%Y-%m-%d'), rates)
        else:
            start_date, start_date_format, rates = getUsdRatesHelper(start_date, start_date_format, end_date_format,
                                                                     rates)
    return rates


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
cache = Cache()

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['200 per day', '50 per hour']
)

app_limit = limiter.shared_limit("200 per minute", scope="API")


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/rates/USD/<ratingDate>', methods=['GET'])
@limiter.limit('60 per minute')
@app_limit
def api_date(ratingDate):
    date_datetime = datetimeSingleDateCheck(ratingDate)
    if cache.has_rate(date_datetime):
        return {ratingDate: cache.day_rates[ratingDate]}
    cache.refresh_check()
    return jsonify(getCorrectUSDRate(date_datetime))


@app.route('/rates/USD/<dateFrom>/<dateTo>', methods=['GET'])
@limiter.limit('10 per minute')
@app_limit
def api_date_from_to(dateFrom, dateTo):
    start_datetime, end_datetime = datetimeDoubleDateCheck(dateFrom, dateTo)
    if cache.has_rates_range(start_datetime, end_datetime):
        return cache.get_rates_range(start_datetime, end_datetime)
    cache.refresh_check()
    return jsonify(getCorrectUSDRates(start_datetime, end_datetime))


@app.route('/sales/<salesDate>', methods=['GET'])
@limiter.limit('60 per minute')
@app_limit
def api_sale(salesDate):
    date_datetime = datetimeSingleDateCheck(salesDate)
    if cache.has_sale(date_datetime):
        return {salesDate: cache.day_sales[salesDate], "sumPLN": cache.day_sales[salesDate]["PLN"], "sumUSD": cache.day_sales[salesDate]["USD"]}
    cache.refresh_check()
    return jsonify(getSalesRate(date_datetime))


@app.route('/sales/<dateFrom>/<dateTo>', methods=['GET'])
@limiter.limit('10 per minute')
@app_limit
def api_sales_from_to(dateFrom, dateTo):
    start_datetime, end_datetime = datetimeDoubleDateCheck(dateFrom, dateTo)
    if cache.has_sales_range(start_datetime, end_datetime):
        return cache.get_sales_range(start_datetime, end_datetime)
    cache.refresh_check()
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
