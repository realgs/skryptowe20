from flask import Flask
from flask_restful import Api

from currency_api import TwoDatesCurrencyRates, OneDayCurrencyRate

app = Flask(__name__)
api = Api(app)

api.add_resource(OneDayCurrencyRate, "/currency-rates/<string:currency>/<string:date>")
api.add_resource(TwoDatesCurrencyRates, "/currency-rates/<string:currency>/<string:start_date>/<string:end_date>")

if __name__ == '__main__':
    app.run(debug=True)
