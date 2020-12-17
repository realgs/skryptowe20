import flask
from flask import request, jsonify, abort
import flask_limiter
from flask_limiter.util import get_remote_address
import sales_data_base
import datetime


CACHE_TIME = datetime.timedelta(hours=1)
NOT_DATE_HTTP_ERROR = (400, '400 BadRequest - Niewlasciwy format daty / Invalid date format')
INVALID_DATE_RANGE_HTTP_ERROR  = (400, '400 BadRequest - Bledny zakres dat / Invalid date range')
NOT_FOUND_IN_BASE_HTTP_ERROR  = (404, '404 NotFound - Brak danych / No data available')
CACHE_EXCHANGE_RATES_PREFIX = 'exchange_rate'
CACHE_SALES_PREFIX = 'sales'


cache = dict()

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

limiter = flask_limiter.Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)


def sales_data_tuples_to_dicts(sales_data_tuples):
    sales_data_dicts = []
    for (date, sales, sales_pln) in sales_data_tuples:
        sales_data_dicts.append({'date' : str(date), 'USD' : sales, 'PLN' : sales_pln})
    return sales_data_dicts


def is_period_in_base(first_day, last_day):
    cache_name = 'first_last_day_base'
    if cache_name not in cache or cache[cache_name][1] < datetime.datetime.now():
        cache[cache_name] = (sales_data_base.get_first_last_day_rates_data(), datetime.datetime.now() + CACHE_TIME)

    first_day_base, last_day_base = cache[cache_name][0]
    return first_day >= first_day_base and last_day <= last_day_base


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Moje API</h1>
<p>Witaj, to jest moje API.</p>
<p>Możesz się z niego dowiedzieć, jakie były notowania USD w latach 2013-2016<br>
oraz jakie były wówczas wartości łącznej sprzedaży </p>
<p>Możliwe zapytania (format daty: RRRR-MM-DD):
    <ul>
        <li>Zapytanie o kurs dolara w dniu "date":<br>
            http://127.0.0.1:5000/api/v1/exchangerates/USD/"date"/</li>
        <li>Zapytanie o kurs dolara od "start_date" do "end_date":<br>
            http://127.0.0.1:5000/api/v1/exchangerates/USD/"start_date"/"end_date"/</li>
        <li>Zapytanie o sumę sprzedaży w dniu "date":<br>
            http://127.0.0.1:5000/api/v1/salesdata/"date"/</li>
        <li>Zapytanie o sumę sprzedaży od "start_date" do "end_date":<br>
            http://127.0.0.1:5000/api/v1/salesdata/"start_date"/"end_date"/</li>
    </ul>
</p>'''


@app.route('/api/v1/exchangerates/USD/<date>/', methods=['GET'])
def api_USD_1day(date):
    try:
        day = sales_data_base.str_to_date(date)
    except:
        abort(NOT_DATE_HTTP_ERROR[0], NOT_DATE_HTTP_ERROR[1])
    
    if not is_period_in_base(day, day):
        abort(NOT_FOUND_IN_BASE_HTTP_ERROR[0], NOT_FOUND_IN_BASE_HTTP_ERROR[1])
    
    cache_name = CACHE_EXCHANGE_RATES_PREFIX + str(day)
    if cache_name not in cache or cache[cache_name][1] < datetime.datetime.now():
        cache[cache_name] = (sales_data_base.get_exchange_rates_data(day, day)[0], datetime.datetime.now() + CACHE_TIME)

    return jsonify(cache[cache_name][0])


@app.route('/api/v1/exchangerates/USD/<start_date>/<end_date>/', methods=['GET'])
def api_USD_start_end(start_date, end_date):
    try:
        first_day = sales_data_base.str_to_date(start_date)
        last_day = sales_data_base.str_to_date(end_date)
    except:
        abort(NOT_DATE_HTTP_ERROR[0], NOT_DATE_HTTP_ERROR[1])

    if(first_day>last_day):
        abort(INVALID_DATE_RANGE_HTTP_ERROR[0], INVALID_DATE_RANGE_HTTP_ERROR[1])

    if not is_period_in_base(first_day, last_day):
        abort(NOT_FOUND_IN_BASE_HTTP_ERROR[0], NOT_FOUND_IN_BASE_HTTP_ERROR[1])
    
    exchange_data = []

    day = first_day
    while day <= last_day:
        cache_name = CACHE_EXCHANGE_RATES_PREFIX + str(day)
        if cache_name not in cache or cache[cache_name][1] < datetime.datetime.now():
            exchange_data = sales_data_base.get_exchange_rates_data(first_day, last_day)
            for exchange_day_data in exchange_data:
                cache_name = CACHE_EXCHANGE_RATES_PREFIX + exchange_day_data['date']
                cache[cache_name] = (exchange_day_data, datetime.datetime.now() + CACHE_TIME)
            day = last_day
        else:
            exchange_data.append(cache[cache_name][0])
        day += datetime.timedelta(days = 1)

    return jsonify(exchange_data)


@app.route('/api/v1/salesdata/<date>/', methods=['GET'])
def api_salesdata_1day(date):
    try:
        day = sales_data_base.str_to_date(date)
    except:
        abort(NOT_DATE_HTTP_ERROR[0], NOT_DATE_HTTP_ERROR[1])

    if not is_period_in_base(day, day):
        abort(NOT_FOUND_IN_BASE_HTTP_ERROR[0], NOT_FOUND_IN_BASE_HTTP_ERROR[1])
    
    cache_name = CACHE_SALES_PREFIX + str(day)
    if cache_name not in cache or cache[cache_name][1] < datetime.datetime.now():
        cache[cache_name] = (sales_data_tuples_to_dicts(sales_data_base.get_sales_data(day, day))[0], datetime.datetime.now() + CACHE_TIME)

    return jsonify(cache[cache_name][0])


@app.route('/api/v1/salesdata/<start_date>/<end_date>/', methods=['GET'])
def api_salesdata_start_end(start_date, end_date):
    try:
        first_day = sales_data_base.str_to_date(start_date)
        last_day = sales_data_base.str_to_date(end_date)
    except:
        abort(NOT_DATE_HTTP_ERROR[0], NOT_DATE_HTTP_ERROR[1])

    if(first_day>last_day):
        abort(INVALID_DATE_RANGE_HTTP_ERROR[0], INVALID_DATE_RANGE_HTTP_ERROR[1])

    if not is_period_in_base(first_day, last_day):
        abort(NOT_FOUND_IN_BASE_HTTP_ERROR[0], NOT_FOUND_IN_BASE_HTTP_ERROR[1])

    sales_data = []

    day = first_day
    while day <= last_day:
        cache_name = CACHE_SALES_PREFIX + str(day)
        if cache_name not in cache or cache[cache_name][1] < datetime.datetime.now():
            sales_data = sales_data_tuples_to_dicts(sales_data_base.get_sales_data(first_day, last_day))
            for sales_day_data in sales_data:
                cache_name = CACHE_SALES_PREFIX + sales_day_data['date']
                cache[cache_name] = (sales_day_data, datetime.datetime.now() + CACHE_TIME)
            day = last_day
        else:
            sales_data.append(cache[cache_name][0])
        day += datetime.timedelta(days = 1)

    return jsonify(sales_data)


app.run()
