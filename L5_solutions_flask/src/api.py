import flask
from flask import abort

import db_getters as db
from constants import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return HOME_INFO


@app.route('/rates/usd/<date>', methods=['GET'])
def usd_rate_specific_date(date):
    date_dt = get_datetime(date)
    if check_date_available(date_dt):
        return db.get_usd_rating(date)


@app.route('/rates/usd/<start_date>/<end_date>', methods=['GET'])
def usd_rate_date_range(start_date, end_date):
    start_date_dt = get_datetime(start_date)
    end_date_dt = get_datetime(end_date)

    if check_date_range_correct(start_date_dt, end_date_dt) and check_date_available(
            start_date_dt) and check_date_available(end_date_dt):
        return db.get_usd_rating_date_range(start_date, end_date)


@app.route('/sales/<date>', methods=['GET'])
def sales_specific_date(date):
    date_dt = get_datetime(date)
    if check_date_available(date_dt):
        return db.get_sales(date)


@app.route('/sales/<start_date>/<end_date>', methods=['GET'])
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
