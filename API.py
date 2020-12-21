from datetime import datetime, date
import flask
from flask import jsonify, abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import NBP_currency
import DB_handler
import const


config = {"DEBUG": True, "CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": const.CACHE_DEFAULT_TIMEOUT}


app = flask.Flask(__name__)
app.config.from_mapping(config)
limiter = Limiter(app, key_func=get_remote_address, default_limits=[const.DAILY_LIMIT, const.HOUR_LIMIT])
appLimiter = limiter.shared_limit(const.CACHE_DEFAULT_TIMEOUT, scope="API")
cache = Cache(app)

def validate_dates(date1, date2):
    try:
        start_datetime = datetime.strptime(date1, "%Y-%m-%d")
        end_datetime = datetime.strptime(date2, "%Y-%m-%d")
    except ValueError:
        abort(const.BAD_REQUEST, description="Wrong date format")
    if date1 > date2:
        abort(const.WRONG_DATE_RANGE, description="Wrong date range")
    if date2 >= str(date.today()):
        abort(const.WRONG_DATE_RANGE, description="Wrong date range")


@app.route('/', methods=['GET'])
def home():
    return ""


@app.route('/sales/<start>/<end>/', methods=['GET'])
@cache.cached()
def api_period_sales(start, end):
    if start < const.ORDERS_MIN_DATE or end > const.ORDERS_MAX_DATE:
        abort(const.WRONG_DATE_RANGE, description="Wrong date range. Start date shouldn't be before" + const.ORDERS_MIN_DATE +
                                            " and end date before " + const.ORDERS_MAX_DATE)
    validate_dates(start, end)
    daily_orders = DB_handler.get_orders_in_pln_and_usd(start, end)
    if daily_orders == {}:
        abort(const.NO_DATA_FOUND, description="No data found")

    else:
        return jsonify(daily_orders)


@app.route('/sales/<search_date>/', methods=['GET'])
@cache.cached()
def api_day_sales(search_date):
    if search_date < const.ORDERS_MIN_DATE or search_date > const.ORDERS_MAX_DATE:
        abort(const.WRONG_DATE_RANGE, description="Wrong date range. Date should be between" + const.ORDERS_MIN_DATE + " and " + const.ORDERS_MAX_DATE)
    validate_dates(search_date, search_date)
    daily_orders = DB_handler.get_orders_in_pln_and_usd(search_date, search_date)
    if daily_orders == {}:
        abort(const.NO_DATA_FOUND, description="No data found")
    else:
        return jsonify(daily_orders)


@app.route('/rates/<currency>/<search_date>/', methods=['GET'])
@cache.cached()
def api_day_rates(currency, search_date):
    if search_date < const.NBP_MIN_DATE:
        abort(const.WRONG_DATE_RANGE, description="Wrong date range. Start date shouldn't be before " + const.NBP_MIN_DATE)
    validate_dates(search_date, search_date)
    rate = NBP_currency.get_daily_currency_rates(search_date, search_date, currency)
    if search_date in rate:
        return jsonify(rate)
    else:
        abort(const.NO_DATA_FOUND, description="No data found")


@app.route('/rates/<currency>/<start>/<end>/', methods=['GET'])
@cache.cached()
def api_period_rates(start, end, currency):
    if start < const.NBP_MIN_DATE:
        abort(const.WRONG_DATE_RANGE, description="Wrong date range. Start date shouldn't be before " + const.NBP_MIN_DATE)
    validate_dates(start, end)
    rates = NBP_currency.get_daily_currency_rates(start, end, currency)
    if start in rates:
        return jsonify(rates)
    else:
        abort(const.NO_DATA_FOUND, description="No data found")


@app.errorhandler(const.NO_DATA_FOUND)
def page_not_found(e):
    return jsonify(error=str(e)), const.NO_DATA_FOUND


@app.errorhandler(const.TOO_MANY_REQUESTS)
def limit_exceeded(e):
    return jsonify(error=str(e)), const.TOO_MANY_REQUESTS


@app.errorhandler(const.WRONG_DATE_RANGE)
def limit_exceeded(e):
    return jsonify(error=str(e)), const.WRONG_DATE_RANGE


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

app.run()