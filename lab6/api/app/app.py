from datetime import datetime
import sqlite3

from flask import Flask, jsonify, g, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

from .database import (
    PATH_TO_DATABASE,
    DatabaseLimits,
    check_if_database_file_exists,
    update_data,
    get_rates_for_dates,
    get_sales_for_dates,
)


app = Flask(__name__)
limiter = Limiter(app, get_remote_address, default_limits=["10/minute;1/second"])
cache = Cache(app, config={"CACHE_TYPE": "simple"})
date_limits = DatabaseLimits()
HOST = "0.0.0.0"
DATE_FORMAT = "%Y-%m-%d"
MAX_DAYS = 366


def get_database():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(PATH_TO_DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def check_date(from_date, to_date, min_date, max_date):
    if to_date < from_date:
        return "date_start cannot be earlier than date_end"

    if (to_date - from_date).days > MAX_DAYS:
        return f"You can only get data for maximum {MAX_DAYS} days at once."

    if from_date < min_date or to_date > max_date:
        return "No data for this period of time."

    return None


@app.route("/api/rates/<string:from_date>/<string:to_date>")
@limiter.limit("100/hour;10/minute/1/second")
@cache.memoize(timeout=300)
def get_rates(from_date, to_date):
    try:
        from_date = datetime.strptime(from_date, DATE_FORMAT).date()
        to_date = datetime.strptime(to_date, DATE_FORMAT).date()
    except ValueError:
        return jsonify(message="Invalid date format"), 400

    message = check_date(
        from_date, to_date, date_limits.min_rates_date, date_limits.max_rates_date
    )

    if message is not None:
        return jsonify(message=message), 400

    connection = get_database()
    rates = get_rates_for_dates(connection, from_date, to_date)

    for entry in rates:
        entry["date"] = entry["date"].strftime(DATE_FORMAT)

    return jsonify(rates=rates)


@app.route("/api/rates/<string:date>")
def get_single_rate(date):
    return redirect(url_for("get_rates", from_date=date, to_date=date))


@app.route("/api/sales/<string:from_date>/<string:to_date>", methods=["GET"])
@cache.memoize(timeout=600)
def get_sales(from_date, to_date):
    try:
        from_date = datetime.strptime(from_date, DATE_FORMAT).date()
        to_date = datetime.strptime(to_date, DATE_FORMAT).date()
    except ValueError:
        return jsonify(message="Invalid date format"), 400

    connection = get_database()
    sales = get_sales_for_dates(connection, from_date, to_date)

    for entry in sales:
        entry["date"] = entry["date"].strftime(DATE_FORMAT)

    return jsonify(sales=sales)


@app.route("/api/sales/<string:date>", methods=["GET"])
@cache.memoize(timeout=600)
def get_single_sale(date):
    return redirect(url_for("get_sales", from_date=date, to_date=date))


def run(args):
    if args.update:
        update_data()
    else:
        check_if_database_file_exists()

    connection = sqlite3.connect(PATH_TO_DATABASE)
    date_limits.load_limits(connection)
    connection.close()

    app.run(host=HOST, port=args.port, debug=args.debug)
