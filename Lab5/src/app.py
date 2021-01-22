from flask import Flask, abort
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime as dt
from flask_cors import CORS

from src import config
from src import database_collector as db

app = Flask(__name__)
app.config["DEBUG"] = True

limiter = Limiter(app, key_func=get_remote_address)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def home():
    return config.HOME_INFO


@app.route('/rates/usd/<date>', methods=['GET'])
@limiter.limit(config.REQUEST_TIME_LIMIT)
@cache.cached(config.CACHE_TIMEOUT)
def usd_rate_on_date(date):
    date_dt = get_datetime_from_str(date)
    if __date_available(date_dt):
        return db.get_usd_rating(date)


@app.route('/rates/usd/<start_date>/<end_date>', methods=['GET'])
@limiter.limit(config.REQUEST_TIME_LIMIT)
@cache.cached(config.CACHE_TIMEOUT)
def usd_rate_on_date_range(start_date, end_date):
    sdt = get_datetime_from_str(start_date)
    edt = get_datetime_from_str(end_date)
    if __start_date_before_end_date_correct(sdt, edt) and __date_available(
            sdt) and __date_available(edt):
        return db.get_usd_rating_date_range(start_date, end_date)


@app.route('/sales/<date>', methods=['GET'])
@limiter.limit(config.REQUEST_TIME_LIMIT)
@cache.cached(config.CACHE_TIMEOUT)
def sales_on_date(date):
    date_dt = get_datetime_from_str(date)
    if __date_available(date_dt):
        return db.get_sales(date)


@app.route('/sales/<start_date>/<end_date>', methods=['GET'])
@limiter.limit(config.REQUEST_TIME_LIMIT)
@cache.cached(config.CACHE_TIMEOUT)
def sales_on_date_range(start_date, end_date):
    sdt = get_datetime_from_str(start_date)
    edt = get_datetime_from_str(end_date)

    if __start_date_before_end_date_correct(sdt, edt) \
            and __date_available(sdt) \
            and __date_available(edt):
        return db.get_sales_date_range(start_date, end_date)


def get_datetime_from_str(date):
    try:
        date_dt = dt.strptime(date, config.DATE_FORMAT)
        return date_dt

    except ValueError:
        abort(400, config.INCORRECT_DATE_FORMAT.format(date=date))


def __date_available(date):
    if config.DATE_RANGE_START <= date <= config.DATE_RANGE_END:
        return True
    else:
        abort(404, config.OUT_OF_RANGE_MSG)


def __start_date_before_end_date_correct(start_date_dt, end_date_dt):
    if end_date_dt < start_date_dt:
        abort(400, config.END_BEFORE_START_MSG)
    else:
        return True


if __name__ == '__main__':
    app.run()
