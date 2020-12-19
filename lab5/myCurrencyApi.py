from datetime import datetime, date
import flask
from flask import jsonify, abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import currencyMethods
import ordersDbMethods

BAD_REQUEST = 400
NO_DATA_FOUND = 404
WRONG_DATE_RANGE = 416
TOO_MANY_REQUESTS = 429
ORDERS_START = '2009-01-01'
ORDERS_END = '2012-12-30'
DEFAULT_LIMIT = "500 per minute"
CACHE_DEFAULT_TIMEOUT = 3600

NBP_MIN_DATE = '2002-01-02'
ORDERS_MIN_DATE = '2009-01-01'
ORDERS_MAX_DATE = '2012-12-30'

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT
}

HOME_SITE = f"""<h1>Prototype of currency rates and sales API</h1>
    <p>API for obtaining different currency rates
    and sales data from Superstore database in USD and PLN.</p>
    <p>With the use of this API you can obtain following data:</p>
     <p> - Chosen currency to PLN exchange rate for specified date:</br>
     http://127.0.0.1:5000/api/v1/resources/rates/chosen_currency/search_date/</br>
         example usage ``http://127.0.0.1:5000/api/v1/resources/rates/eur/2010-09-09/``</p>
     <p> - Chosen currency to PLN exchange rate for date range:</br>
     http://127.0.0.1:5000/api/v1/resources/rates/chosen_currency/start/end/</br>
         example usage ``http://127.0.0.1:5000/api/v1/resources/rates/eur/2018-10-10/2019-10-10/``</br>
     <p> - sales data for specified date:</br>
     http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/search_date/</br>
         example usage ``http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/2010-10-10/``</br>
     <p> - sales data for date range:</br>
     http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/start/end/</br>
         example usage ``http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/2010-10-10/2011-10-10/``</br>
    <p> Orders data is available for date range: 
    {ORDERS_START} - {ORDERS_END}</p>
    <p>Note, that there is a limit for requests: {DEFAULT_LIMIT} per user. 
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
    CACHE_DEFAULT_TIMEOUT,
    scope="myCurrencyApi"
)
cache = Cache(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def validate_dates(date1, date2):
    try:
        start_datetime = datetime.strptime(date1, "%Y-%m-%d")
        end_datetime = datetime.strptime(date2, "%Y-%m-%d")
    except ValueError:
        abort(BAD_REQUEST, description="Wrong date format, it should be in ISO 8601 format i.e. 2010-12-31")

    if date1 > date2:
        abort(WRONG_DATE_RANGE, description="Wrong date range. Start date should be before ends date")
    if date2 >= str(date.today()):
        abort(WRONG_DATE_RANGE, description="Wrong date range. Date should be before today's date")


@app.route('/', methods=['GET'])
def home():
    return HOME_SITE


@app.route('/api/v1/resources/orders/dailyOrders/<start>/<end>/', methods=['GET'])
@cache.cached()
@appLimiter
@limiter.limit("100 per minute")
def api_daily_orders_days(start, end):
    if start < ORDERS_MIN_DATE or end > ORDERS_MAX_DATE:
        abort(WRONG_DATE_RANGE, description="Wrong date range. Start date shouldn't be before" + ORDERS_MIN_DATE +
                                            " and end date before " + ORDERS_MAX_DATE)
    validate_dates(start, end)
    daily_orders = ordersDbMethods.get_orders_in_pln_and_usd(start, end)
    if daily_orders == {}:
        abort(NO_DATA_FOUND, description="No data found")

    else:
        return daily_orders


@app.route('/api/v1/resources/orders/dailyOrders/<search_date>/', methods=['GET'])
@cache.cached()
@appLimiter
@limiter.limit("300 per minute")
def api_daily_orders_day(search_date):
    if search_date < ORDERS_MIN_DATE or search_date > ORDERS_MAX_DATE:
        abort(WRONG_DATE_RANGE, description="Wrong date range. Date should be between" + ORDERS_MIN_DATE + " and " + ORDERS_MAX_DATE)
    validate_dates(search_date, search_date)
    daily_orders = ordersDbMethods.get_orders_in_pln_and_usd(search_date, search_date)
    if daily_orders == {}:
        abort(NO_DATA_FOUND, description="No data found")
    else:
        return daily_orders


@app.route('/api/v1/resources/rates/<currency>/<search_date>/', methods=['GET'])
@cache.cached()
@appLimiter
@limiter.limit("300 per minute")
def api_rates_day(currency, search_date):
    if search_date < NBP_MIN_DATE:
        abort(WRONG_DATE_RANGE, description="Wrong date range. Start date shouldn't be before " + NBP_MIN_DATE)
    validate_dates(search_date, search_date)
    rate = currencyMethods.get_daily_currency_rates(search_date, search_date, currency)
    if search_date in rate:
        return jsonify(rate)
    else:
        abort(NO_DATA_FOUND, description="No data found")


@app.route('/api/v1/resources/rates/<currency>/<start>/<end>/', methods=['GET'])
@cache.cached()
@appLimiter
@limiter.limit("100 per minute")
def api_rates_days(start, end, currency):
    if start < NBP_MIN_DATE:
        abort(WRONG_DATE_RANGE, description="Wrong date range. Start date shouldn't be before " + NBP_MIN_DATE)
    validate_dates(start, end)
    rates = currencyMethods.get_daily_currency_rates(start, end, currency)
    if start in rates:
        return jsonify(rates)
    else:
        abort(NO_DATA_FOUND, description="No data found")


@app.errorhandler(NO_DATA_FOUND)
def page_not_found(e):
    return jsonify(error=str(e)), NO_DATA_FOUND


@app.errorhandler(TOO_MANY_REQUESTS)
def limit_exceeded(e):
    return jsonify(error=str(e)), TOO_MANY_REQUESTS


@app.errorhandler(WRONG_DATE_RANGE)
def limit_exceeded(e):
    return jsonify(error=str(e)), WRONG_DATE_RANGE


app.run()
