from flask import Flask
from flask_restful import Api, Resource
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import database as db
import rates_api_handler as rah
import sales_api_handler as sah
import database_handler as dbh
import data_file as df

cursor = db.connect()

app = Flask(__name__)
api = Api(app)
app.config["CACHE_TYPE"] = df.CACHE_TYPE

cache = Cache()
cache.init_app(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[df.DEFAULT_LIMIT]
)


class CurrencyRates(Resource):
    @cache.cached(timeout=df.CACHE_TIMEOUT)
    def get(self, currency, date_from, date_to):
        currency = currency.upper()
        error_message = rah.create_error_json(currency, date_from, date_to)
        if error_message is not None:
            return error_message

        currency_rates = db.get_currency_rate_data_between_date(cursor, date_from, date_to)
        json_format = rah.convert_to_json_format(currency_rates)
        return {
                   'result': {
                       'base currency': 'USD',
                       'exchanged currency': currency,
                       'rates': json_format
                   }
               }, 200


class CurrencySales(Resource):
    @cache.cached(timeout=df.CACHE_TIMEOUT)
    def get(self, currency, date):
        currency = currency.upper()
        error_massage = sah.create_error_json(currency, date)
        if error_massage is not None:
            return error_massage

        base_currency_sales = float("{:.2f}".format(
            dbh.get_daily_sales(cursor, date, currency)
        ))
        exchanged_currency_sales = float("{:.2f}".format(
            base_currency_sales * db.get_currency_rate_of_day(cursor, date, currency)
        ))

        return {
                   'result': {
                       'date': date,
                       'sales': [
                           {
                               'base currency': 'USD',
                               'value': base_currency_sales
                           },
                           {
                               'exchanged currency': currency,
                               'value': exchanged_currency_sales
                           }
                       ]
                   }
               }, 200


api.add_resource(CurrencyRates, '/rates/<string:currency>/<string:date_from>/<string:date_to>')
api.add_resource(CurrencySales, '/sales/<string:currency>/<string:date>')

if __name__ == "__main__":
    app.run(debug=True)
