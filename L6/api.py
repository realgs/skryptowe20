#!/usr/bin/python3

import datetime
import flask
from flask import request, jsonify, make_response, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


import database


# basic configuration
TABLES_URI = '/api/v1/exchangerates/tables/'
RATES_URI = '/api/v1/exchangerates/rates/'
SALES_URI = '/api/v1/sales/'
DAILY_LIMIT = "200 per day"
MINUTE_LIMIT = "30 per minute"
CACHE_LIFETIME = 120 # seconds
sales_cache = {}

app = flask.Flask(__name__)
limiter = Limiter(
    app,
    key_func = get_remote_address,
    default_limits = [DAILY_LIMIT, MINUTE_LIMIT]
)

def string_to_datetime(date_string):
    try: date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError: return False
    return date

def error_message(message, code = 400):
    return { 'error': { 'code' : code, 'message' : message } }

def beutify_markings(markings):
    markings_array = []

    for (date, rate, currency_code, interpolated) in markings:
        if interpolated: markings_array.append( { 'date': date, 'rate': rate, 'currency': currency_code, 'interpolated': True } )
        else: interpolated: markings_array.append( { 'date': date, 'rate': rate, 'currency': currency_code, 'interpolated': False } )

    return markings_array

def get_sales_from_cache(date_from):
    if date_from in sales_cache and sales_cache[date_from]['cached on'] + datetime.timedelta(seconds = CACHE_LIFETIME) > datetime.datetime.now() :
        return sales_cache[date_from]
    else:
        row = database.get_daily_sales(date_from)
        row.update({ 'cached on' : datetime.datetime.now() })
        sales_cache.update({ date_from : row })
        return row


@app.route("/ping")
@limiter.exempt
def ping():
    return {"response":"PONG"}


@app.route('/', methods=['GET'])
def home():
    return render_template("public/index.html")
    #
    # '''
    #     <h1>Forex&Sales API</h1>
    #     <p>More to see @ <a href="https://github.com/japko-7/skryptowe20/tree/L5">GitHub</a>.</p>
    # '''


@app.errorhandler(400)
def bad_request(e):
    return error_message(400, "Bad request."), 400

@app.errorhandler(403)
def access_forbidden(e):
    return error_message(403, "You don't have permission to the resource."), 403

@app.errorhandler(404)
def page_not_found(e):
    return error_message(404, "The resource could not be found."), 404

@app.errorhandler(429)
def page_not_found(e):
    return error_message(404, "Limit of requests exceeded."), 429

@app.errorhandler(500)
def server_error(e):
    return error_message(500, "Internal server error. Please try again later."), 500


# tables
@app.route( TABLES_URI )
def get_all_markings():
    return jsonify(beutify_markings(database.get_table("markings")))

@app.route( TABLES_URI + 'today' )
def get_all_today_markings():
    return jsonify(beutify_markings(database.get_all_daily_markings(datetime.datetime.now())))

@app.route( TABLES_URI + 'last/<int:top_count>' )
def get_last_markings(top_count):
    if top_count < 0: return error_message(400, 'Request for less then 0 items.'), 400

    markings = database.get_limited_table("markings", top_count)
    if len(markings) < top_count:
        return jsonify([ ('markings served', len(markings)) ] + beutify_markings(markings))
    else:
        return jsonify(beutify_markings(markings))

@app.route( TABLES_URI + '<string:date>' )
def get_all_daily_markings(date):
    datetime = string_to_datetime(date)
    oldest_date = database.get_oldest_marking_date()
    newest_date = database.get_newest_marking_date()

    if not datetime: return error_message(400, 'Invalid date format.'), 400
    if date < oldest_date: return error_message(404, 'Markings older than ' + oldest_date + ' are not available.'), 404
    if date > newest_date: return error_message(404, 'Markings newer than ' + newest_date + ' are not available.'), 404

    return jsonify(beutify_markings(database.get_all_daily_markings(datetime)))

@app.route( TABLES_URI + '<string:start_date>/<string:end_date>' )
def get_all_markings_from_period(start_date, end_date):
    date_from = string_to_datetime(start_date)
    date_to = string_to_datetime(end_date)
    oldest_date = database.get_oldest_marking_date()
    newest_date = database.get_newest_marking_date()

    if not date_from: return error_message(400, 'Invalid start date format.'), 400
    if not date_to: return error_message(400, 'Invalid end date format.'), 400
    if date_to < date_from: return error_message(400, 'End date greater than start date.'), 400
    if start_date < oldest_date: return error_message(404, 'Markings older than ' + oldest_date + ' are not available.'), 404
    if end_date > newest_date: return error_message(404, 'Markings newer than ' + newest_date + ' are not available.'), 404

    return jsonify(beutify_markings(database.get_markings_from_period(date_from, date_to)))


# rates
@app.route( RATES_URI + '<string:currency_code>/' )
def get_all_currency_markings(currency_code):
    if not database.check_currency_availability(currency_code): return  error_message(400, 'Unsupported currency code.'), 400
    return jsonify(beutify_markings(database.get_all_currency_markings(currency_code)))

@app.route( RATES_URI + '<string:currency_code>/today' )
def get_currnecy_today_markings(currency_code):
    if not database.check_currency_availability(currency_code): return  error_message(400, 'Unsupported currency code.'), 400
    return jsonify(beutify_markings(database.get_currency_daily_markings(currency_code, datetime.datetime.now())))

@app.route( RATES_URI + '<string:currency_code>/last/<int:top_count>' )
def get_last_currency_markings(currency_code, top_count):

    if not database.check_currency_availability(currency_code): return  error_message(400, 'Unsupported currency code.'), 400
    if top_count < 0: return error_message(400, 'Request for less then 0 items.'), 400

    markings = database.get_limited_currency_markings(currency_code, top_count)

    if len(markings) < top_count:
        return jsonify([ ('markings served', len(markings)) ] + beutify_markings(markings))
    else:
        return jsonify(beutify_markings(markings))

@app.route( RATES_URI + '<string:currency_code>/<string:date>' )
def get_currency_daily_markings(currency_code, date):

    if not database.check_currency_availability(currency_code): return error_message(400, 'Unsupported currency code.'), 400

    datetime = string_to_datetime(date)
    oldest_date = database.get_oldest_marking_date(currency_code)
    newest_date = database.get_newest_marking_date(currency_code)

    if not datetime: return error_message(400, 'Invalid date format.'), 400
    if date < oldest_date: return error_message(404, 'Markings older than ' + oldest_date + ' are not available.'), 404
    if date > newest_date: return error_message(404, 'Markings newer than ' + newest_date + ' are not available.'), 404

    return jsonify(beutify_markings(database.get_currency_daily_markings(currency_code, datetime)))

@app.route( RATES_URI + '<string:currency_code>/<string:start_date>/<string:end_date>' )
def get_currency_markings_from_period(currency_code, start_date, end_date):

    if not database.check_currency_availability(currency_code): return error_message(400, 'Unsupported currency code.'), 400

    date_from = string_to_datetime(start_date)
    date_to = string_to_datetime(end_date)
    oldest_date = database.get_oldest_marking_date(currency_code)
    newest_date = database.get_newest_marking_date(currency_code)

    if not date_from: return error_message(400, 'Invalid start date format.'), 400
    if not date_to: return error_message(400, 'Invalid end date format.'), 400
    if date_to < date_from: return error_message(400, 'End date greater than start date.'), 400
    if start_date < oldest_date: return error_message(404, 'Markings older than ' + oldest_date + ' are not available.'), 404
    if end_date > newest_date: return error_message(404, 'Markings newer than ' + newest_date + ' are not available.'), 404

    return jsonify(beutify_markings(database.get_currency_markings_from_period(currency_code, date_from, date_to)))


# sales
@app.route( SALES_URI + '<string:date>' )
def get_daily_sales(date):

    datetime = string_to_datetime(date)
    oldest_date = database.get_oldest_sale_date()
    newest_date = database.get_newest_sale_date()

    if not datetime: return error_message(400, 'Invalid date format.'), 400
    if date < oldest_date: return error_message(404, 'Sales older than ' + oldest_date + ' are not available.'), 404
    if date > newest_date: return error_message(404, 'Sales newer than ' + newest_date + ' are not available.'), 404

    return get_sales_from_cache(datetime)

@app.route( SALES_URI + '<string:start_date>/<string:end_date>' )
def get_sales_from_period(start_date, end_date):

    date_from = string_to_datetime(start_date)
    date_to = string_to_datetime(end_date)
    oldest_date = database.get_oldest_sale_date()
    newest_date = database.get_newest_sale_date()

    if not date_from: return error_message(400, 'Invalid start date format.'), 400
    if not date_to: return error_message(400, 'Invalid end date format.'), 400
    if date_to < date_from: return error_message(400, 'End date greater than start date.'), 400
    if start_date < oldest_date: return error_message(404, 'Sales older than ' + oldest_date + ' are not available.'), 404
    if end_date > newest_date: return error_message(404, 'Sales newer than ' + newest_date + ' are not available.'), 404

    result = []

    while date_from <= date_to:
        result += [get_sales_from_cache(date_from)]
        date_from = date_from + datetime.timedelta(1)

    return jsonify(result)

def run_app():
    app.run()
