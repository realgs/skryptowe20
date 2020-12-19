from flask import Flask
from flask_restful import Api, Resource
import L5_API.db_manager as db_mgr


app = Flask(__name__)
api = Api(app)


class Rates(Resource):
    def get(self, currency):
        date = db_mgr.get_todays_date(currency)
        rate = db_mgr.get_rate(date, currency)
        return {"currency": currency, "rates": [
            {"date": date},
            {"rate": rate}]}


api.add_resource(Rates, "/rates/<string:currency>")


if __name__ == "__main__":
    app.run(debug=True)
