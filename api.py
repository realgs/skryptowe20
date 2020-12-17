import flask
import datetime
import requests
import pandas as pd
import db_handler
from flask import jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


API_URL = "http://api.nbp.pl/api/exchangerates/rates/A/usd"
DATE_FORMAT = "%Y-%m-%d"
DAYS_LIMIT = 365
RATES_FROM_LIMIT = "2002-01-02"
SALES_FROM_LIMIT = "2012-07-04"
SALES_TO_LIMIT = "2016-02-19"
DEFAULT_REQUEST_LIMIT = "20/minute"
DEFAULT_CACHE_TIMEOUT = 100


def get_usd_exchange_rate(date):
    initial_date = date
    result = {}
    while len(result.keys()) == 0:
        request_url = f"{API_URL}/{date}/"
        response = requests.get(request_url)
        if response.status_code == 200:
            result['rate'] = {"date": initial_date, "rate": response.json()['rates'][0]['mid'],
                              "interpolated": not date == initial_date}
        else:
            try:
                date = datetime.datetime.strptime(date, DATE_FORMAT)
            except ValueError:
                return page_not_found(404)
            if date < datetime.datetime.strptime(RATES_FROM_LIMIT, DATE_FORMAT) or date > datetime.datetime.today():
                return date_out_of_range(400)
            date -= datetime.timedelta(days=1)
            date = date.strftime(DATE_FORMAT)

    return jsonify(result)


def get_usd_exchange_rate_from_to(date_from, date_to):
    try:
        date_from = datetime.datetime.strptime(date_from, DATE_FORMAT)
        local_date_to = datetime.datetime.strptime(date_to, DATE_FORMAT)
    except ValueError:
        return page_not_found(404)

    dates_delta = (local_date_to - date_from).days
    cur_dates = []
    cur_rates = []

    if (local_date_to - date_from).days < 0:
        return range_not_satisfiable(416)
    if date_from < datetime.datetime.strptime(RATES_FROM_LIMIT,
                                              DATE_FORMAT) or local_date_to > datetime.datetime.today():
        return date_out_of_range(400)

    while dates_delta >= 0:
        if dates_delta >= DAYS_LIMIT:
            local_date_to = date_from + datetime.timedelta(days=DAYS_LIMIT - 1)

        local_date_to = local_date_to.strftime(DATE_FORMAT)
        date_from = date_from.strftime(DATE_FORMAT)

        request_url = f"{API_URL}/{date_from}/{local_date_to}/"
        response = requests.get(request_url)

        cur_dates += [(i['effectiveDate']) for i in response.json()["rates"]]
        cur_rates += [i["mid"] for i in response.json()["rates"]]
        local_date_to = datetime.datetime.strptime(local_date_to, DATE_FORMAT)
        date_from = local_date_to
        local_date_to = datetime.datetime.strptime(date_to, DATE_FORMAT)

        dates_delta -= DAYS_LIMIT

    return cur_dates, cur_rates


def fill_missing_data(date_from, date_to, dates, rates):
    date_from = datetime.datetime.strptime(date_from, DATE_FORMAT)
    date_to = datetime.datetime.strptime(date_to, DATE_FORMAT)
    all_dates = pd.date_range(date_from, date_to, freq='d').format()
    all_rates = []
    interpolated = []
    results = []

    for i in range(len(all_dates)):
        starting_from_missing_satisfied = False
        if all_dates[i] in dates:
            all_rates.append(rates[dates.index(all_dates[i])])
            interpolated.append(False)
        else:
            interpolated.append(True)
            if len(all_rates) != 0:
                all_rates.append(all_rates[len(all_rates) - 1])
            else:
                while not starting_from_missing_satisfied:
                    date_from -= datetime.timedelta(days=1)
                    date_from = date_from.strftime(DATE_FORMAT)
                    request_url = f"{API_URL}/{date_from}/"
                    response = requests.get(request_url)
                    if response.status_code == 200:
                        all_rates.append(response.json()['rates'][0]['mid'])
                        starting_from_missing_satisfied = True
                    date_from = datetime.datetime.strptime(date_from, DATE_FORMAT)

    for i in range(len(all_dates)):
        results.append({"rate": {"date": all_dates[i], "rate": all_rates[i], "interpolated": interpolated[i]}})

    return results


def get_sales(date):
    try:
        date = datetime.datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        return page_not_found(404)
    if date < datetime.datetime.strptime(SALES_FROM_LIMIT, DATE_FORMAT) or\
            date > datetime.datetime.strptime(SALES_TO_LIMIT, DATE_FORMAT):
        return date_out_of_range(400)

    result = {}
    values = db_handler.get_sales_data(date.strftime(DATE_FORMAT))
    result['sales'] = {"date": values[0][0], "sales_usd": values[0][1], "sales_pln": values[0][2]}
    return jsonify(result)


def get_sales_from_to(date_from, date_to):
    try:
        date_from = datetime.datetime.strptime(date_from, DATE_FORMAT)
        date_to = datetime.datetime.strptime(date_to, DATE_FORMAT)
    except ValueError:
        return page_not_found(404)

    if (date_to - date_from).days < 0:
        return range_not_satisfiable(416)
    if date_from < datetime.datetime.strptime(RATES_FROM_LIMIT,
                                              DATE_FORMAT) or date_to > datetime.datetime.today():
        return date_out_of_range(400)

    results = []
    values = db_handler.get_sales_data_from_to(date_from.strftime(DATE_FORMAT), date_to.strftime(DATE_FORMAT))
    for i in range(len(values)):
        results.append({"sales": {"date": values[i][0], "sales_usd": values[i][1], "sales_pln": values[i][2]}})
    return jsonify(results)


app = flask.Flask(__name__)
app.config["DEBUG"] = True

limiter = Limiter(app, key_func=get_remote_address)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return "<h1>script languages - list 5</h1>"


@app.route('/api/rates/USD/<date>', methods=['GET'])
@limiter.limit(DEFAULT_REQUEST_LIMIT)
@cache.cached(DEFAULT_CACHE_TIMEOUT)
def usd_rate_at(date):
    return get_usd_exchange_rate(date)


@app.route('/api/rates/USD/<date_from>/<date_to>', methods=['GET'])
@limiter.limit(DEFAULT_REQUEST_LIMIT)
@cache.cached(DEFAULT_CACHE_TIMEOUT)
def usd_rate_from_to(date_from, date_to):
    check = get_usd_exchange_rate_from_to(date_from, date_to)
    if list(map(type, check)) == [str, int]:
        return check
    else:
        return jsonify(fill_missing_data(date_from, date_to, check[0], check[1]))


@app.route('/api/sales/<date>', methods=['GET'])
@limiter.limit(DEFAULT_REQUEST_LIMIT)
@cache.cached(DEFAULT_CACHE_TIMEOUT)
def sales_at(date):
    return get_sales(date)


@app.route('/api/sales/<date_from>/<date_to>', methods=['GET'])
@limiter.limit(DEFAULT_REQUEST_LIMIT)
@cache.cached(DEFAULT_CACHE_TIMEOUT)
def sales_from_to(date_from, date_to):
    return get_sales_from_to(date_from, date_to)


@app.errorhandler(400)
def date_out_of_range(e):
    return "<h1>400: Date is out of range</h1>", 400


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404: PageNotFound</h1>", 404


@app.errorhandler(416)
def range_not_satisfiable(e):
    return "<h1>416: Range Not Satisfiable</h1>", 416


app.run()
