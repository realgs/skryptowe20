from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api

from currencies_api import TwoDatesCurrencyRates, OneDayCurrencyRate
from sales_api import OneDateSalesForCurrency, TwoDatesSalesForCurrency

app = Flask(__name__)
api = Api(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per second"]
)

api.add_resource(OneDayCurrencyRate, "/currency-rates/<string:currency>/<string:date>")
api.add_resource(TwoDatesCurrencyRates, "/currency-rates/<string:currency>/<string:start_date>/<string:end_date>")

api.add_resource(OneDateSalesForCurrency, "/sales/<string:currency>/<string:date>")
api.add_resource(TwoDatesSalesForCurrency, "/sales/<string:currency>/<string:start_date>/<string:end_date>")

if __name__ == '__main__':
    app.run(debug=True)
