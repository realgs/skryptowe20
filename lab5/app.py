from flask import Flask
from flask_restful import Api, Resource
import datetime as dt
import database as db

MY_DB_DATE_FROM = "2011-10-01"
MY_DB_DATE_TO = "2014-05-28"

app = Flask(__name__)
api = Api(app)
cursor = db.connect()


class CurrencyRates(Resource):
    def get(self, currency, date_from, date_to):
        currency = currency.upper()
        error_message = create_error_json(currency, date_from, date_to)
        if error_message is not None:
            return error_message

        currency_rates = db.get_currency_rate_data_between_date(cursor, date_from, date_to)
        json_format = convert_to_json_format(currency_rates)
        return {
                   "result": {
                       "base_currency": "USD",
                       "final_currency": currency,
                       "rates": json_format
                   }
               }, 200


api.add_resource(CurrencyRates, "/rates/<string:currency>/<string:date_from>/<string:date_to>")


def create_error_json(currency, date_from, date_to):
    currency_is_correct = check_currency_available(currency)
    dates_format = check_date_format(date_from) & check_date_format(date_to)
    if dates_format:
        dates_range = check_date_range(date_from) & check_date_range(date_to)
    else:
        dates_range = False

    if not currency_is_correct:
        if dates_format:
            return create_error_message("Invalid currency. Currency not found."), 404
        return create_error_message("Invalid request"), 400
    if not dates_format:
        return create_error_message("Invalid date format. Admissible: YYYY-MM-DD"), 400
    if not dates_range:
        return create_error_message("Data out of range selected. Allowed range from " +
                                    MY_DB_DATE_FROM + " to " + MY_DB_DATE_TO)
    return None


def check_currency_available(currency):
    return currency == "PLN"


def check_date_format(date):
    if len(date) == 10:
        for i in range(len(date)):
            if not (i == 4 or i == 7):
                if not date[i].isnumeric():
                    return False
    else:
        return False
    return True


def check_date_range(date):
    date_to_check = dt.datetime.strptime(date, '%Y-%m-%d')
    if date_to_check < dt.datetime.strptime(MY_DB_DATE_FROM, '%Y-%m-%d') or \
            date_to_check > dt.datetime.strptime(MY_DB_DATE_TO, '%Y-%m-%d'):
        return False
    return True


def create_error_message(message):
    return {"message": message}


def convert_to_json_format(list):
    new_list = []
    for row in list:
        new_list.append({
            "date": str((row[0]))[:10],
            "mid": row[1],
            "interpolated": row[3]
        })
    return new_list


if __name__ == "__main__":
    app.run(debug=True)
