from flask import Flask, Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from db_connection import get_rates_from_to, update_rates_table_to_day, initialize_db, get_profit_in_currencies
from threading import Timer
import datetime
import decimal
import json


app = Flask(__name__)
# Used to limit number of requests per user // task 4
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5/minute"],
)

first_rate_measure_db = datetime.datetime.strptime('2015-12-21', '%Y-%m-%d')
# Assume that rates will be updated by 21:00, otherwise they get interpolated
update_at_hour = 21

rates_cache = []
profit_cache = []


# Used to serialize data returned by endpoints
# https://stackoverflow.com/a/22238613
def json_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError ("Type %s not serializable" % type(obj))


# Task 1 and 2 endpoint
@app.route('/rates/from/<date_from>/to/<date_to>', methods=['GET'])
def get_rates(date_from='', date_to=''):
    try:
        date_from_parsed = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to_parsed = datetime.datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        return Response('Invalid date format', status=400)
    if date_from_parsed > date_to_parsed:
        return Response('date_from cannot be greater than date_to', status=400)
    if date_from_parsed < first_rate_measure_db or date_to_parsed > datetime.datetime.today() - datetime.timedelta(days=1):
        first_rate_measure_db_str = datetime.datetime.strftime(first_rate_measure_db, '%Y-%m-%d')
        today_str = datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=1), '%Y-%m-%d')
        return Response('Date interval must be between ' + first_rate_measure_db_str + ' and ' + today_str, status=400)
    #result = get_rates_from_to(date_from, date_to)
    result = []
    for entry in rates_cache:
        entry_date = entry['date']
        app.logger.warning(entry['date'])
        if entry_date >= date_from_parsed and entry_date <= date_to_parsed:
            result.append(entry)
    return Response(json.dumps(result, default=json_serializer), status=200)


# Task 3 endpoint
@app.route('/profits/day/<summary_date>', methods=['GET'])
def get_profit(summary_date=''):
    try:
        summary_date_parsed = datetime.datetime.strptime(summary_date, '%Y-%m-%d')
    except ValueError:
        return Response('Invalid date format', status=400)
    if summary_date_parsed < first_rate_measure_db or summary_date_parsed > datetime.datetime.today() - datetime.timedelta(days=1):
        first_rate_measure_db_str = datetime.datetime.strftime(first_rate_measure_db, '%Y-%m-%d')
        today_str = datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=1), '%Y-%m-%d')
        return Response('Date must be between ' + first_rate_measure_db_str + ' and ' + today_str, status=400)
    for entry in profit_cache:
        if summary_date_parsed == datetime.datetime.strptime(entry['date'], '%Y-%m-%d'):
            return Response(json.dumps(entry, default=json_serializer), status=200)
    return Response(json.dumps({'date':summary_date_parsed, 'profit_usd':0.0, 'profit_pln':0.0}, default=json_serializer), status=200)


# Call timer_callback at initial_date
def setup_timer(initial_date, offset_secs):
    now = datetime.datetime.now()
    diff = initial_date - now

    t = Timer(diff.seconds, lambda : timer_callback(offset_secs))
    t.daemon = True
    t.start()


# Update values in db and start another timer
def timer_callback(offset_secs):
    update_rates_table_to_day(datetime.datetime.today() - datetime.timedelta(days=1))
    update_cache()
    t = Timer(offset_secs, lambda : timer_callback(offset_secs))
    t.daemon = True
    t.start()


def update_cache(to_day):
    # Cache rates
    first_rate_measure_db_str = datetime.datetime.strftime(first_rate_measure_db, '%Y-%m-%d')
    to_day_str = datetime.datetime.strftime(to_day, '%Y-%m-%d')
    global rates_cache
    rates_cache = get_rates_from_to(first_rate_measure_db_str, to_day_str)

    global profit_cache
    profit_cache = get_profit_in_currencies(first_rate_measure_db_str, to_day_str)


if __name__ == '__main__':
    #initialize_db()
    # Setup timer that will update values every day at update_at_hour
    initial_date = datetime.datetime.now()
    initial_date = initial_date.replace(hour=update_at_hour, minute=0, second=0)
    if initial_date < datetime.datetime.now():
        initial_date.replace(day=initial_date.day+1)
    setup_timer(initial_date, 86400) # 86400 = 1 day in seconds
    
    # Update values in db on init
    update_rates_table_to_day(datetime.datetime.today() - datetime.timedelta(days=1))

    # Load cache on init
    to_day = datetime.datetime.today() - datetime.timedelta(days=1)
    update_cache(to_day)
    app.logger.warning(len(profit_cache))

    # Start server
    app.run(debug=True)
    # todo caching 
    # todo readme 
    # todo screeny xd?
    # todo task 3
