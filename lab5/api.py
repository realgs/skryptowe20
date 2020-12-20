from flask import Flask
from flask_restful import Api, Resource
import datetime as dt

from connectDB import connect, get_currency_rate_data_between_date

MY_DB_DATE_FROM = "2011-10-01"
MY_DB_DATE_TO = "2014-05-28"

app = Flask(__name__)
api = Api(app)
cursor = connect()


class CurrencyRates(Resource):
    def get(self, currency_id, date_from, date_to):
        currency_id = currency_id.upper()
        if currency_id == "USD":
            if check_date_format(date_from) & check_date_format(date_to):
                if check_date_range(date_from) & check_date_range(date_from):
                    currency_rate = get_currency_rate_data_between_date(cursor, date_from, date_to)
                    print(currency_rate)
                    json_list = currency_rate_list_to_json_format(currency_rate)
                    print(json_list)
                    wynik = {
                        "currency": currency_id,
                        "rates": json_list
                    }
                    print(wynik)
                    return wynik
                else:
                    return {"error": 400, "description": "Data out of range selected. Allowed range from " + MY_DB_DATE_FROM + " to " + MY_DB_DATE_TO}
            else:
                return {"error": 400, "description": "Invalid date format entered. Admissible: YYYY-MM-DD"}
        else:
            return {"error": 404, "description": "Currency not found"}


api.add_resource(CurrencyRates, "/rates/<string:currency_id>/<string:date_from>/<string:date_to>")


def currency_rate_list_to_json_format(data):
    list = []
    for row in data:
        list.append({
            "date": str(__datetime_with_time_converter(row[0]))[:10],
            "mid_rate": row[1],
            "is_interpolated": row[2]
        })
    return list


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
    if dt.datetime.strptime(date_string, '%Y-%m-%d') > dt.datetime.strptime(MY_DB_DATE_FROM, '%Y-%m-%d') or \
            dt.datetime.strptime(date_string, '%Y-%m-%d') < dt.datetime.strptime(MY_DB_DATE_TO, '%Y-%m-%d'):
        return False
    return True


if __name__ == "__main__":
    app.run(debug=True)
