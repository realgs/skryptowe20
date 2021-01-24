from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api, Resource
import datetime as dt

from company import get_daily_turnover
from connectDB import connect, get_currency_rate_data_between_date, get_currency_rate_of_day

MY_DB_DATE_FROM = "2011-10-01"
MY_DB_DATE_TO = "2014-05-28"
AVAILABLE_CURRENCIES = ['AUD', 'BYN', 'BGN', 'HRK', 'DKK',
                        'JPY', 'CAD', 'NOK', 'CZK', 'RUB',
                        'RON', 'PLN', 'CHF', 'SEK', 'TRY',
                        'EUR', 'UAH', 'HUF', 'GBP']

app = Flask(__name__)
api = Api(app)
cursor = connect()
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minutes"]
)


class CurrencyRates(Resource):
    def get(self, currency_id, date_from, date_to):
        currency_id = currency_id.upper()
        if currency_id == "PLN":
            if check_date_format(date_from) & check_date_format(date_to):
                if check_date_range(date_from) & check_date_range(date_from):
                    currency_rate = get_currency_rate_data_between_date(cursor, date_from, date_to)
                    json_list = currency_rate_list_to_json_format(currency_rate)
                    return {
                        "status": 200,
                        "result": {
                            "base_currency": "USD",
                            "final_currency": currency_id,
                            "rates": json_list
                        }
                    }
                else:
                    return {"status": 400, "description": "Data out of range selected. Allowed range from " +
                                                          MY_DB_DATE_FROM + " to " + MY_DB_DATE_TO}
            else:
                return {"status": 400, "description": "Invalid date format entered. Admissible: YYYY-MM-DD"}
        else:
            return {"status": 404, "description": "Currency not found"}


api.add_resource(CurrencyRates, "/rates/<string:currency_id>/<string:date_from>/<string:date_to>")


class DailyTurnover(Resource):
    def get(self, date, currency_id):
        currency_id = currency_id.upper()
        if AVAILABLE_CURRENCIES.__contains__(str(currency_id)):
            if check_date_format(date):
                if check_date_range(date):
                    default_currency_turnover_value = float("{:.2f}".format(get_daily_turnover(cursor, date,
                                                                                               currency_id)))
                    value_turnover_selected_currency = float("{:.2f}".format(default_currency_turnover_value *
                                                                             get_currency_rate_of_day(cursor, date,
                                                                                                      currency_id)))
                    return {
                        "status": 200,
                        "result": {
                            "date": date,
                            "turnover": [
                                {
                                    "currency": "USD",
                                    "value": default_currency_turnover_value
                                },
                                {
                                    "currency": currency_id,
                                    "value": value_turnover_selected_currency
                                }
                            ]
                        }
                    }
                else:
                    return {"status": 400, "description": "Data out of range selected. Allowed range from " +
                                                          MY_DB_DATE_FROM + " to " + MY_DB_DATE_TO}
            else:
                return {"status": 400, "description": "Invalid date format entered. Admissible: YYYY-MM-DD"}
        else:
            return {"status": 404, "description": "Currency not found"}


api.add_resource(DailyTurnover, "/turnover/<string:date>/<string:currency_id>")


def currency_rate_list_to_json_format(data):
    new_list = []
    for row in data:
        new_list.append({
            "date": str(__datetime_with_time_converter(row[0]))[:10],
            "mid_rate": row[1],
            "is_interpolated": row[3]
        })
    return new_list


def __datetime_with_time_converter(string_datetime):
    return dt.datetime.strptime(str(string_datetime), '%Y-%m-%d %H:%M:%S')


def check_date_format(date_string):
    if len(date_string) == 10:
        for i in range(len(date_string)):
            if not (i == 4 or i == 7):
                if not date_string[i].isnumeric():
                    return False
    else:
        return False
    return True


def check_date_range(date_string):
    dt.datetime.strptime(date_string, '%Y-%m-%d')
    if dt.datetime.strptime(date_string, '%Y-%m-%d') < dt.datetime.strptime(MY_DB_DATE_FROM, '%Y-%m-%d') or \
            dt.datetime.strptime(date_string, '%Y-%m-%d') > dt.datetime.strptime(MY_DB_DATE_TO, '%Y-%m-%d'):
        return False
    return True


if __name__ == "__main__":
    app.run(debug=True)
