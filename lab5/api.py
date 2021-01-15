from datetime import datetime
import flask
from flask import jsonify, abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import db_getters

INVALID_REQUEST_CODE = 400
NO_DATA_FOUND_CODE = 404
INVALID_DATE_RANGE_CODE = 416
TOO_MANY_REQUESTS_CODE = 429

START_DATE = '2018-07-04'
END_DATE = '2020-05-06'

DEFAULT_LIMIT = "400 per minute"
USER_LIMIT = "50 per minute"
CACHE_DEFAULT_TIMEOUT = 86400

DATE_FORMAT = '%Y-%m-%d'

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT
}

HOME_SITE_INFO = f"""<h1>USD currency rates and product sales API</h1>
    <p>With this API you can obtain following data:</p>
     <p> - sales data for specified date:</br>
     http://127.0.0.1:5000/api/sales/{{date}}/</br>
         example \"http://127.0.0.1:5000/api/sales/2018-08-08/\"</br>
     <p> - sales data for date range:</br>
     http://127.0.0.1:5000/api/sales/{{start_date}}/{{end_date}}/</br>
         example \"http://127.0.0.1:5000/api/sales/2018-10-10/2019-10-10/\"</br>
     <p> - USD to PLN exchange rate for specified date:</br>
     http://127.0.0.1:5000/api/rates/{{date}}/</br>
         example \"http://127.0.0.1:5000/api/rates/2018-07-13/\"</p>
     <p> - USD to PLN exchange rate for dates range:</br>
     http://127.0.0.1:5000/api/rates/{{start_date}}/{{end_date}}/</br>
         example \"http://127.0.0.1:5000/api/rates/2018-10-10/2019-10-10/\"</br>
    <p> Sales and exchange rates data is available for date range: 
    {START_DATE} - {END_DATE}</p>
    <p>There is a limit for requests: {DEFAULT_LIMIT}. 
    Cache timeout is set to {CACHE_DEFAULT_TIMEOUT} seconds.</p>
"""

app = flask.Flask(__name__)
app.config.from_mapping(config)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

appLimiter = limiter.shared_limit(
    DEFAULT_LIMIT,
    scope="myapi"
)
cache = Cache(app)


def check_dates(start_date, end_date):
    try:
        datetime.strptime(start_date, DATE_FORMAT)
        datetime.strptime(end_date, DATE_FORMAT)
    except ValueError:
        abort(INVALID_REQUEST_CODE,
              description="Invalid date format. Date should be in ISO 8601 format i.e. 2018-01-01")

    if start_date > end_date:
        abort(INVALID_DATE_RANGE_CODE,
              description="Invalid date range. The start date should be earlier than the end date")


@app.route('/', methods=['GET'])
def home():
    return HOME_SITE_INFO


@app.route('/api/sales/<sales_date>/', methods=['GET'])
@appLimiter
@limiter.limit(USER_LIMIT)
@cache.cached()
def api_sales_on_date(sales_date):
    if sales_date < START_DATE or sales_date > END_DATE:
        abort(INVALID_DATE_RANGE_CODE,
              description="Invalid date. Date should be between" + START_DATE + " and " + END_DATE)
    check_dates(sales_date, sales_date)
    sales = db_getters.get_sales_from_day(sales_date)
    if sales:
        return jsonify(sales)
    else:
        abort(NO_DATA_FOUND_CODE, description="No data found")


@app.route('/api/sales/<start_date>/<end_date>/', methods=['GET'])
@appLimiter
@limiter.limit(USER_LIMIT)
@cache.cached()
def api_sales_between_dates(start_date, end_date):
    if start_date < START_DATE or end_date > END_DATE:
        abort(INVALID_DATE_RANGE_CODE,
              description="Invalid date range. Start date should not be earlier than " + START_DATE +
                          " and end date not later than " + END_DATE)
    check_dates(start_date, end_date)
    sales = db_getters.get_sales_between_days(start_date, end_date)
    if sales:
        return jsonify(sales)
    else:
        abort(NO_DATA_FOUND_CODE, description="No data found")


@app.route('/api/rates/<rate_date>/', methods=['GET'])
@appLimiter
@limiter.limit(USER_LIMIT)
@cache.cached()
def api_rate_at_date(rate_date):
    if rate_date < START_DATE:
        abort(INVALID_DATE_RANGE_CODE,
              description="Invalid date. Date should be between" + START_DATE + " and " + END_DATE)
    check_dates(rate_date, rate_date)
    rate = db_getters.get_usd_prices_from_date(rate_date)
    if rate:
        return jsonify(rate)
    else:
        abort(NO_DATA_FOUND_CODE, description="No data found")


@app.route('/api/rates/<start_date>/<end_date>/', methods=['GET'])
@appLimiter
@limiter.limit(USER_LIMIT)
@cache.cached()
def api_rates_between_dates(start_date, end_date):
    if start_date < START_DATE or end_date > END_DATE:
        abort(INVALID_DATE_RANGE_CODE,
              description="Invalid date range. Start date should not be earlier than " + START_DATE +
                          " and end date not later than " + END_DATE)
    check_dates(start_date, end_date)
    rates = db_getters.get_usd_prices_between_dates(start_date, end_date)
    if rates:
        return jsonify(rates)
    else:
        abort(NO_DATA_FOUND_CODE, description="No data found")


@app.errorhandler(NO_DATA_FOUND_CODE)
def page_not_found(e):
    return jsonify(error=str(e)), NO_DATA_FOUND_CODE


@app.errorhandler(TOO_MANY_REQUESTS_CODE)
def limit_exceeded(e):
    return jsonify(error=str(e)), TOO_MANY_REQUESTS_CODE


@app.errorhandler(INVALID_DATE_RANGE_CODE)
def limit_exceeded(e):
    return jsonify(error=str(e)), INVALID_DATE_RANGE_CODE


app.run()
