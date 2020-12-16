from datetime import datetime

import flask
from flask import jsonify

import lab5.db_service as db_service

DATE_FORMAT = "%y-%m-%d"

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def check_date(str_date):
    isValidDate = True
    try:
        year, month, day = str_date.split('-')
        datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    return isValidDate


@app.route('/api/rates/usd/<date>', methods=['GET'])
def get_rate_for_one_day(date):
    if not check_date(date):
        return jsonify({'message': 'Entered date is not correct'})
    else:
        data = db_service.get_usd_exchange_rate_for_one_day(date)
        if data is None:
            return jsonify({'message': 'Brak danych dla tej daty'})
        else:
            return jsonify({'date': data['date'], 'rate': data['rate'], 'interpolated': data['interpolated']})


@app.route('/api/rates/usd/<start_date>/<end_date>', methods=['GET'])
def get_rate_for_days_range(start_date, end_date):
    if not (check_date(start_date) and check_date(end_date)):
        return jsonify({'message': 'Entered date is not correct'})
    elif datetime.strptime(db_service.get_usd_exchange_min_date(), "%Y-%m-%d").date() > datetime.strptime(start_date, "%Y-%m-%d").date() or datetime.strptime(db_service.get_usd_exchange_max_date(), "%Y-%m-%d").date() < datetime.strptime(end_date, "%Y-%m-%d").date():
        return jsonify({'message': 'No data for this date range'})
    else:
        data = db_service.get_usd_exchange_rate_for_days_range(start_date, end_date)
        if data is None:
            return jsonify({'message': 'Brak danych dla tego zakresu'})
        else:
            return jsonify(data)


app.run()
print("Input date is not valid..")
