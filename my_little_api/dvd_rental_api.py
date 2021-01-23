import asyncio
import threading
from datetime import datetime

import flask
import sqlalchemy
from flask import jsonify, request, abort
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import to_dictionary

app = flask.Flask(__name__)
app.config["DEBUG"] = False

DB_URI = "postgres://postgres:bazman@localhost:5432/dvdrental"
engine = sqlalchemy.create_engine(DB_URI)
conn = engine.connect()
Base = automap_base()
Base.prepare(conn, reflect=True)

# cache
last_update_date = datetime.fromisoformat('1000-12-12')
exchange_rates_cache = {}
payments_cache = {}
min_date = None
max_date = None

# banlist
ip_list = {}
white_list = {'127.0.0.1'}


@app.before_request
def count_and_block():
    ip = request.environ.get('REMOTE_ADDR')
    print("Ip = " + ip)
    if ip not in white_list:
        if ip in ip_list:
            if ip_list[ip]['is_banned']:
                abort(429)
            else:
                ip_list[ip]['count'] += 1
                if ip_list[ip]['count'] > 5:
                    ip_list[ip]['is_banned'] = True
                    abort(429)
    else:
        ip_list[ip] = {'count': 0, 'is_banned': False}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/', methods=['GET'])
def home():
    return "<h1>DVD Rental Shop API</h1><p>This site is a prototype API for checking certaind DVD rental shop sales.</p>"


@app.route('/api/v1/resources/exchangerates', methods=['GET'])
def api_exchangerates():
    start_date = None
    end_date = None
    results = {}
    index = 0

    # Get Variables
    if 'startdate' in request.args:
        try:
            start_date = datetime.strptime(request.args['startdate'], '%d/%m/%y').date()
            if start_date < min_date:
                abort(400, "DECLARED START DATE LOWER THAN MIN DATE. OMIT PARAMETER TO USE MIN DATE.")
            if start_date > max_date:
                abort(400, "DECLARED START DATE HIGHER THAN MAX DATE. OMIT PARAMETER TO USE MIN DATE.")
        except ValueError:
            abort(400, "WRONG START DATE FORMAT. PLEASE USE DD/MM/YY FORMAT.")

    if 'enddate' in request.args:
        try:
            end_date = datetime.strptime(request.args['enddate'], '%d/%m/%y').date()
            if end_date < min_date:
                abort(400, "DECLARED END DATE LOWER THAN MIN DATE. OMIT PARAMETER TO USE MAX DATE.")
            if end_date > max_date:
                abort(400, "DECLARED END DATE HIGHER THAN MAX DATE. OMIT PARAMETER TO USE MAX DATE.")
            if 'startdate' in request.args and end_date < start_date:
                abort(400, "DECLARED END DATE LOWER THAN MIN DATE. OMIT PARAMETER TO USE MAX DATE.")
        except ValueError:
            abort(400, "WRONG END DATE FORMAT. PLEASE USE DD/MM/YY FORMAT.")

    # Process
    if start_date is not None:
        if end_date is not None:
            for i in range(exchange_rates_cache.__len__()):
                if start_date <= exchange_rates_cache[i]['date'] <= end_date:
                    results[index] = exchange_rates_cache[i]
                    index += 1
        else:
            for i in range(exchange_rates_cache.__len__()):
                if start_date <= exchange_rates_cache[i]['date']:
                    results[index] = exchange_rates_cache[i]
                    index += 1
    else:
        if end_date is not None:
            for i in range(exchange_rates_cache.__len__()):
                if exchange_rates_cache[i]['date'] <= end_date:
                    results[index] = exchange_rates_cache[i]
                    index += 1
        else:
            results = exchange_rates_cache

    # Return
    return jsonify(results)


@app.errorhandler(400)
def api_error400(error):
    return jsonify(error.description)


@app.route('/api/v1/resources/salessummary', methods=['GET'])
def api_salessummary():
    results = {'COUNT': 0, 'SUM_IN_USD': 0, 'SUM_IN_PLN': 0}
    date = None

    # Get Variables
    if 'date' in request.args:
        try:
            date = datetime.strptime(request.args['date'], '%d/%m/%y').date()
            if date < min_date:
                abort(400, "DECLARED DATE LOWER THAN MIN DATE. OMIT PARAMETER TO GET LATEST SUMMARY.")
            if date > max_date:
                abort(400, "DECLARED DATE HIGHER THAN MAX DATE. OMIT PARAMETER TO GET LATEST SUMMARY.")
        except ValueError:
            abort(400, "WRONG DATE FORMAT. PLEASE USE DD/MM/YY FORMAT.")
    else:
        abort(400, "MISSING REQUIRED PARAMETER: DATE.")

    # Process
    if date is not None:
        for i in range(payments_cache.__len__()):
            if payments_cache[i]['payment_date'] == date:
                results['COUNT'] += 1
                results['SUM_IN_USD'] += payments_cache[i]['amount']
                results['SUM_IN_PLN'] += payments_cache[i]['amount_in_PLN']

    # Return
    return jsonify(results)


@app.route('/api/v1/resources/salessummary/range', methods=['GET'])
def api_salessummaryrange():
    start_date = None
    end_date = None
    results = {'COUNT': 0, 'SUM_IN_USD': 0, 'SUM_IN_PLN': 0}

    # Get Variables
    if 'startdate' in request.args:
        try:
            start_date = datetime.strptime(request.args['startdate'], '%d/%m/%y').date()
            if start_date < min_date:
                abort(400, "DECLARED START DATE LOWER THAN MIN DATE. OMIT PARAMETER TO USE MIN DATE.")
            if start_date > max_date:
                abort(400, "DECLARED START DATE HIGHER THAN MAX DATE. OMIT PARAMETER TO USE MIN DATE.")
        except ValueError:
            abort(400, "WRONG START DATE FORMAT. PLEASE USE DD/MM/YY FORMAT.")

    if 'enddate' in request.args:
        try:
            end_date = datetime.strptime(request.args['enddate'], '%d/%m/%y').date()
            if end_date < min_date:
                abort(400, "DECLARED END DATE LOWER THAN MIN DATE. OMIT PARAMETER TO USE MAX DATE.")
            if end_date > max_date:
                abort(400, "DECLARED END DATE HIGHER THAN MAX DATE. OMIT PARAMETER TO USE MAX DATE.")
            if 'startdate' in request.args and end_date < start_date:
                abort(400, "DECLARED END DATE LOWER THAN MIN DATE. OMIT PARAMETER TO USE MAX DATE.")
        except ValueError:
            abort(400, "WRONG END DATE FORMAT. PLEASE USE DD/MM/YY FORMAT.")

    # Process
    if start_date is not None:
        if end_date is not None:
            for i in range(payments_cache.__len__()):
                if start_date <= payments_cache[i]['payment_date'] <= end_date:
                    results['COUNT'] += 1
                    results['SUM_IN_USD'] += payments_cache[i]['amount']
                    results['SUM_IN_PLN'] += payments_cache[i]['amount_in_PLN']
        else:
            for i in range(payments_cache.__len__()):
                if start_date <= payments_cache[i]['payment_date']:
                    results['COUNT'] += 1
                    results['SUM_IN_USD'] += payments_cache[i]['amount']
                    results['SUM_IN_PLN'] += payments_cache[i]['amount_in_PLN']
    else:
        if end_date is not None:
            for i in range(payments_cache.__len__()):
                if payments_cache[i]['payment_date'] <= end_date:
                    results['COUNT'] += 1
                    results['SUM_IN_USD'] += payments_cache[i]['amount']
                    results['SUM_IN_PLN'] += payments_cache[i]['amount_in_PLN']
        else:
            for i in range(payments_cache.__len__()):
                results['COUNT'] += 1
                results['SUM_IN_USD'] += payments_cache[i]['amount']
                results['SUM_IN_PLN'] += payments_cache[i]['amount_in_PLN']

    # Return
    return jsonify(results)


async def update(delay):
    global last_update_date
    global ip_list
    if datetime.today().date() > last_update_date.date():
        print("UPDATING CACHE")
        last_update_date = datetime.today()
        # We are refreshing whole cache instead of just appending new dates, to update old values in case of any edits.
        Session = sessionmaker(bind=conn)
        session = Session()
        global exchange_rates_cache
        exchange_rates_cache = to_dictionary.model_to_dict(session.query(Base.classes.exchange_rate.date,
                                                                         Base.classes.exchange_rate.usd_to_pln,
                                                                         Base.classes.exchange_rate.interpolated).all())
        global payments_cache
        payments_cache = to_dictionary.model_to_dict(session.query(Base.classes.payment.amount,
                                                                   Base.classes.payment.payment_date).all())
        for i in range(payments_cache.__len__()):
            exchange_rate_found = False
            payments_cache[i]['amount'] = float(payments_cache[i]['amount'])
            for j in range(exchange_rates_cache.__len__()):
                if exchange_rates_cache[j]['date'] == payments_cache[i]['payment_date']:
                    payments_cache[i]['amount_in_PLN'] = payments_cache[i]['amount'] * exchange_rates_cache[j][
                        'usd_to_pln']
                    exchange_rate_found = True
                    break
            if not exchange_rate_found:
                payments_cache[i]['amount_in_PLN'] = 0
        global min_date
        min_date = exchange_rates_cache[0]['date']
        global max_date
        max_date = exchange_rates_cache[exchange_rates_cache.__len__() - 1]['date']
    print("CLEANING IP LIST")
    ip_list = {}
    await asyncio.sleep(delay)


async def update_loop():
    while True:
        await update(60)


def start_update_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


loop = asyncio.get_event_loop()
t = threading.Thread(target=start_update_loop, args=(loop,), daemon=True)
t.start()
task = asyncio.run_coroutine_threadsafe(update_loop(), loop)
app.run()
