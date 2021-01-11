from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api, Resource

import currencies_api
import sales_api
from api_date_checker_and_parser import parse_str_to_date

DEFAULT_LIMIT = "1 per second"
CACHE_TYPE = "simple"
CACHE_TIMEOUT = 7200

app = Flask(__name__)
api = Api(app)
app.config["CACHE_TYPE"] = CACHE_TYPE

cache = Cache()
cache.init_app(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[DEFAULT_LIMIT]
)


class TwoDatesCurrencyRates(Resource):
    @cache.cached(timeout=CACHE_TIMEOUT)
    def get(self, currency, start_date, end_date):
        error_msg = currencies_api.get_error_json_with_code_for_data(currency, start_date, end_date)
        if error_msg is not None:
            return error_msg

        start_date = parse_str_to_date(start_date)
        end_date = parse_str_to_date(end_date)
        rates = currencies_api.get_currency_rates(currency, start_date, end_date)
        return currencies_api.create_json_from_rates(rates, currency)


class OneDayCurrencyRate(Resource):
    @cache.cached(timeout=CACHE_TIMEOUT)
    def get(self, currency, date):
        error_msg = currencies_api.get_error_json_with_code_for_data(currency, date)
        if error_msg is not None:
            return error_msg

        date = parse_str_to_date(date)
        rates = currencies_api.get_currency_rates(currency, date, date)
        return currencies_api.create_json_from_rates(rates, currency)


class TwoDatesSalesForCurrency(Resource):
    @cache.cached(timeout=CACHE_TIMEOUT)
    def get(self, currency, start_date, end_date):
        error_msg = sales_api.get_error_json_with_code_for_data(currency, start_date, end_date)
        if error_msg is not None:
            return error_msg

        start_date = parse_str_to_date(start_date)
        end_date = parse_str_to_date(end_date)
        sales = sales_api.get_sales_for_date_and_currency(currency, start_date, end_date)
        return sales_api.create_json_from_sales(sales, currency)


class OneDateSalesForCurrency(Resource):
    @cache.cached(timeout=CACHE_TIMEOUT)
    def get(self, currency, date):
        error_msg = sales_api.get_error_json_with_code_for_data(currency, date)
        if error_msg is not None:
            return error_msg

        date = parse_str_to_date(date)
        sales = sales_api.get_sales_for_date_and_currency(currency, date, date)
        return sales_api.create_json_from_sales(sales, currency)


api.add_resource(OneDayCurrencyRate, "/currency-rates/<string:currency>/<string:date>")
api.add_resource(TwoDatesCurrencyRates, "/currency-rates/<string:currency>/<string:start_date>/<string:end_date>")

api.add_resource(OneDateSalesForCurrency, "/sales/<string:currency>/<string:date>")
api.add_resource(TwoDatesSalesForCurrency, "/sales/<string:currency>/<string:start_date>/<string:end_date>")

if __name__ == '__main__':
    app.run(debug=True)
