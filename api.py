import flask
from flask import jsonify
import cache
from validate_operations import check_date, check_dates
from constans import NO_DATA_FOUND, OK, to_datetime, REQUEST_LIMIT_RATE, REQUEST_LIMIT_SALE, APPLICATION_REQUEST_LIMIT
import db_operations
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(__name__)
app.config['DEBUG'] = True
limiter = Limiter(app=app, key_func=get_remote_address, application_limits=APPLICATION_REQUEST_LIMIT)


def run():
    db_operations.db_init()
    app.run()


@app.route('/', methods=['GET'])
def home():
    return """<div style="text-align: center">
              <h1>Kaggle Sales API<br></h1>
              <h2>Piotr Swirkaitis - 246753</h2>
              <p>Availible endpoints: </p>
              <p>RATES </p>
              <p>USD to PLN exchange rate for specified date:
    -    http://127.0.0.1:5000/rates/{date}<br></p>  
              <p>USD to PLN exchange rate for specified period: 
    -   http://127.0.0.1:5000/rates/{start_date}/{end_date}<br> <br></p>
              <p>SALES </p>
              <p>sales data in USD and PLN for specified date:
    -   http://127.0.0.1:5000/sales/{date} <br></p>
              <p> sales data in USD and PLN for specified period: 
    -   http://127.0.0.1:5000/sales/{start_date}/{end_date} </p></div>"""


@app.route('/rates/<date_string>', methods=['GET'])
@limiter.limit(REQUEST_LIMIT_RATE)
def get_rate_date(date_string):
    found_rate = {}
    ret_code = check_date(date_string)
    if ret_code != OK:
        return jsonify(ret_code.message), ret_code.code

    if cache.has_rate(date_string):
        return jsonify(cache.rates_cache[date_string]), OK.code

    data = db_operations.get_rates_for_day(date_string)

    if not data:
        return jsonify(NO_DATA_FOUND.message), NO_DATA_FOUND.code
    else:
        found_rate[data[0][0]] = {'date': data[0][1], 'usd_rate': data[0][1], 'interpolated': data[0][2]}
        cache.rates_cache[date_string] = found_rate

    return jsonify(found_rate), ret_code.code


@app.route('/rates/<date_start>/<date_end>', methods=['GET'])
@limiter.limit(REQUEST_LIMIT_RATE)
def get_rates_dates(date_start, date_end):
    found_rates = {}
    ret_code = check_dates(date_start, date_end)

    if ret_code != OK:
        return jsonify(ret_code.message), ret_code.code

    dates = cache.has_rate_range(to_datetime(date_start), to_datetime(date_end))
    if dates:
        return jsonify(cache.get_rates_from_range(dates)), OK.code

    data = db_operations.get_rates_for_dates(date_start, date_end)

    if not data:
        return jsonify(NO_DATA_FOUND.message), NO_DATA_FOUND.code

    else:
        for date, rate, interpolated in data:
            found_rates[date] = {'date': date, 'usd_rate': rate, 'interpolated': interpolated}
            cache.rates_cache[date] = found_rates[date]

    return jsonify(found_rates), ret_code.code


@app.route('/sales/<date_string>', methods=['GET'])
@limiter.limit(REQUEST_LIMIT_SALE)
def get_sale_date(date_string):
    found_sale = {}
    ret_code = check_date(date_string)
    if ret_code != OK:
        return jsonify(ret_code.message), ret_code.code

    if cache.has_sale(date_string):
        if not cache.sales_cache[date_string]:
            return jsonify(NO_DATA_FOUND.message), NO_DATA_FOUND.code

        return jsonify(cache.sales_cache[date_string]), OK.code

    data = db_operations.get_sales_sum_for_day(date_string)

    if not data:
        return jsonify(NO_DATA_FOUND.message), NO_DATA_FOUND.code
    else:
        found_sale[data[0][1]] = {'date': data[0][1], 'usd_rate': data[0][2], 'usd_sale_sum': round(data[0][0], 4),
                                  'pln_sale_sum': round(float(data[0][0] * data[0][2]), 4)}
        cache.sales_cache[date_string] = found_sale

    return jsonify(found_sale), ret_code.code


@app.route('/sales/<date_start>/<date_end>', methods=['GET'])
@limiter.limit(REQUEST_LIMIT_SALE)
def get_sales_dates(date_start, date_end):
    found_sales = {}
    ret_code = check_dates(date_start, date_end)

    if ret_code != OK:
        return jsonify(ret_code.message), ret_code.code

    dates, range_date = cache.has_request((to_datetime(date_start), to_datetime(date_end)))
    if dates:
        sales = cache.get_sales_from_range(range_date)
        if not sales:
            return jsonify(NO_DATA_FOUND.message), NO_DATA_FOUND.code

        return jsonify(sales), OK.code

    data = db_operations.get_sales_sum_for_dates(date_start, date_end)

    if not data:
        return jsonify(NO_DATA_FOUND.message), NO_DATA_FOUND.code

    else:
        cache.requests_cache.append(range_date)
        for order_sum, date, rate in data:
            found_sales[date] = {'date': date, 'usd_rate': rate, 'usd_sale_sum': round(order_sum, 4),
                                 'pln_sale_sum': round(float(rate * order_sum), 4)}
            cache.sales_cache[date] = found_sales[date]

    return jsonify(found_sales), ret_code.code
