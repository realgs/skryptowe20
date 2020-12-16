from datetime import datetime

import flask
from flask import abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import db_getters as db
import conf
from utils import DATA_DATE_RANGE_START, DATE_FORMAT, DATA_DATE_RANGE_END

HOME_INFO = f"""<h1>Northwind Sales API</h1>
    <p>API for obtaining USD and PLN daily exchange rates and sales data from Northwind database in USD and PLN.</p>
    <p>With the use of this API you can obtain following data:</p>
     <p> - USD to PLN exchange rate for specified date:</br>
     http://127.0.0.1:5000/rates/usd/{{date}}</br>
         example usage ``http://127.0.0.1:5000/rates/usd/2013-01-01</p>
     <p> - USD to PLN exchange rate for specified date:</br>
     http://127.0.0.1:5000/rates/usd/{{start_date}}/{{end_date}}</br>
         example usage ``http://127.0.0.1:5000/rates/usd/2013-01-01/2014-12-31``</br>
     <p> - sales data for specified date:</br>
     http://127.0.0.1:5000/sales/{{date}}</br>
         example usage ``http://127.0.0.1:5000/sales/2013-01-01</br>
     <p> - USD to PLN exchange rate for specified date:</br>
     http://127.0.0.1:5000/sales/{{start_date}}/{{end_date}}</br>
         example usage ``http://127.0.0.1:5000/sales/2013-01-01/2014-12-31``</br>

    <p> Data is available for date range: 
    {DATA_DATE_RANGE_START.strftime(DATE_FORMAT)} - {DATA_DATE_RANGE_END.strftime(DATE_FORMAT)}</p>

    <p>Note, that there is a limit for requests: {conf.DEFAULT_LIMIT} per user. 
    Cache timeout is set to {conf.DEFAULT_CACHE_TIMEOUT}.</p>
"""

ABORT_OUT_OF_RANGE_MSG = f"""No data found. Note that data is available only for date range: 
    {DATA_DATE_RANGE_START.strftime(DATE_FORMAT)} - {DATA_DATE_RANGE_END.strftime(DATE_FORMAT)}"""

ABORT_END_BEFORE_START_MSG = "End date cannot be earlier than start date."
ABORT_INCORRECT_DATE_FORMAT = f"Incorrect date format: {{date}}. Required date format: {DATE_FORMAT}"

app = flask.Flask(__name__)
app.config["DEBUG"] = True

limiter = Limiter(app, key_func=get_remote_address)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return HOME_INFO


@app.route('/rates/usd/<date>', methods=['GET'])
@limiter.limit(conf.DEFAULT_LIMIT)
@cache.cached(conf.DEFAULT_CACHE_TIMEOUT)
def usd_rate_specific_date(date):
    date_dt = get_datetime(date)
    if check_date_available(date_dt):
        return db.get_usd_rating(date)


@app.route('/rates/usd/<start_date>/<end_date>', methods=['GET'])
@limiter.limit(conf.DEFAULT_LIMIT)
@cache.cached(conf.DEFAULT_CACHE_TIMEOUT)
def usd_rate_date_range(start_date, end_date):
    start_date_dt = get_datetime(start_date)
    end_date_dt = get_datetime(end_date)

    if check_date_range_correct(start_date_dt, end_date_dt) and check_date_available(
            start_date_dt) and check_date_available(end_date_dt):
        return db.get_usd_rating_date_range(start_date, end_date)


@app.route('/sales/<date>', methods=['GET'])
@limiter.limit(conf.DEFAULT_LIMIT)
@cache.cached(conf.DEFAULT_CACHE_TIMEOUT)
def sales_specific_date(date):
    date_dt = get_datetime(date)
    if check_date_available(date_dt):
        return db.get_sales(date)


@app.route('/sales/<start_date>/<end_date>', methods=['GET'])
@limiter.limit(conf.DEFAULT_LIMIT)
@cache.cached(conf.DEFAULT_CACHE_TIMEOUT)
def sales_date_range(start_date, end_date):
    start_date_dt = get_datetime(start_date)
    end_date_dt = get_datetime(end_date)

    if check_date_range_correct(start_date_dt, end_date_dt) and check_date_available(
            start_date_dt) and check_date_available(end_date_dt):
        return db.get_sales_date_range(start_date, end_date)


def get_datetime(date):
    try:
        date_dt = datetime.strptime(date, DATE_FORMAT)
        return date_dt

    except ValueError:
        abort(400, ABORT_INCORRECT_DATE_FORMAT.format(date=date))


def check_date_available(date):
    if DATA_DATE_RANGE_START <= date <= DATA_DATE_RANGE_END:
        return True
    else:
        abort(404, ABORT_OUT_OF_RANGE_MSG)


def check_date_range_correct(start_date_dt, end_date_dt):
    if end_date_dt < start_date_dt:
        abort(400, ABORT_END_BEFORE_START_MSG)
    else:
        return True


app.run()
