import decimal
import flask.json
from datetime import date, datetime
from operator import itemgetter
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dbManager import DataAccessObject
from nbpRatesReceiver import get_currency_rates
from salesDataCalculator import SalesDataCalculator
from validation import validate_rates_request, validate_sales_request
from logging.config import dictConfig
from flask_cors import CORS, cross_origin

DB_CONFIG = '../../docker-db-config.json'
REQUESTS_LIMIT_PER_ADDRESS = '10/second'

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s][%(levelname)s][%(module)s]: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, datetime) or isinstance(obj, date):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


def limit_per_address_call_exceeded(e):
    message = f'Too many requests! Your requests limit is: {e.description}.'
    return {'errorType': 'TooManyRequestsError', 'messages': [message]}, 429


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = MyJSONEncoder
app.register_error_handler(429, limit_per_address_call_exceeded)
limiter = Limiter(app, key_func=get_remote_address)
dao = DataAccessObject(DB_CONFIG)
rates_supplier = lambda currency_code, date: get_currency_rates(currency_code, date, date)
salesDataCalculator = SalesDataCalculator(dao, rates_supplier)


@app.route('/api/rates/<currency_code>')
@cross_origin()
@limiter.limit(REQUESTS_LIMIT_PER_ADDRESS)
def receive_rates(currency_code):
    is_proper_request, params_or_errors = validate_rates_request(currency_code, request.args)
    if is_proper_request:
        currency_code, start_date, end_date = itemgetter('currencyCode', 'startDate', 'endDate')(params_or_errors)
        try:
            return get_currency_rates(currency_code, start_date, end_date), 200
        except Exception as exc:
            return {'errorType': 'InternalConnectionError', 'messages': str(exc)}, 500
    else:
        return {'errorType': 'ValidationError', 'messages': params_or_errors}, 404


# All Daily calculations are cached. All prices are calculated only once. Then they are taken from cache
@app.route('/api/sales/<currency_code>')
@cross_origin()
@limiter.limit(REQUESTS_LIMIT_PER_ADDRESS)
def receive_sales(currency_code):
    is_proper_request, params_or_errors = validate_sales_request(currency_code, request.args)
    if is_proper_request:
        currency_code, date = itemgetter('currencyCode', 'date')(params_or_errors)
        try:
            amount_in_pln = salesDataCalculator.calculate_sales_amount('PLN', date)
            amount_in_currency = salesDataCalculator.calculate_sales_amount(currency_code, date)
            return {
                       "totalOrdersAmountInPLN": amount_in_pln,
                       f"totalOrdersAmountIn{currency_code}": amount_in_currency
                   }, 200
        except Exception as exc:
            return {'errorType': 'InternalConnectionError', 'messages': str(exc)}, 500
    else:
        return {'errorType': 'ValidationError', 'messages': params_or_errors}, 404


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
