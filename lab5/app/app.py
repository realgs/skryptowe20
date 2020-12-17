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
    load_limits,
    update_data,
    get_rates_for_dates,
    get_sales_for_date,
)


app = Flask(__name__)
limiter = Limiter(app, get_remote_address, default_limits=["10/minute;1/second"])
cache = Cache(app, config={"CACHE_TYPE": "simple"})
date_limits = DatabaseLimits()
HOST = "0.0.0.0"
DATE_FORMAT = "%Y-%m-%d"


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


@app.route("/rates/<string:from_date>/<string:to_date>")
@limiter.limit("100/hour;10/minute/1/second")
@cache.memoize(timeout=300)
def get_rates(from_date, to_date):
    try:
        from_date = datetime.strptime(from_date, DATE_FORMAT).date()
        to_date = datetime.strptime(to_date, DATE_FORMAT).date()
    except ValueError:
        return jsonify(message="Invalid date format"), 400

    if to_date < from_date:
        return jsonify(message="date_start cannot be earlier than date_end"), 400

    if (to_date - from_date).days > 366:
        return (
            jsonify(message="You can only get data for maximum 366 days at once."),
            400,
        )

    if from_date < date_limits.min_rates_date or to_date > date_limits.max_rates_date:
        return jsonify(message="No data for this period of time.")

    connection = get_database()
    rates = get_rates_for_dates(connection, from_date, to_date)

    for entry in rates:
        entry["date"] = entry["date"].strftime(DATE_FORMAT)

    return jsonify(rates=rates)


@app.route("/rates/<string:date>")
def get_single_rate(date):
    return redirect(url_for("get_rates", from_date=date, to_date=date))


@app.route("/sales/<string:date>", methods=["GET"])
@cache.memoize(timeout=600)
def get_sales(date):
    try:
        date = datetime.strptime(date, DATE_FORMAT).date()
    except ValueError:
        return jsonify(message="Invalid date format"), 400

    if date < date_limits.min_sales_date or date > date_limits.max_sales_date:
        return jsonify(message="No data for this date.")

    connection = get_database()
    sales = get_sales_for_date(connection, date)

    if not sales:
        sales = {"date": date, "original_total": 0, "exchanged_total": 0}

    sales["date"] = sales["date"].strftime(DATE_FORMAT)
    return jsonify(sales=sales)


def run(args):
    if args.update:
        update_data()
    else:
        check_if_database_file_exists()

    load_limits(date_limits)
    app.run(host=HOST, port=args.port, debug=args.debug)
