from flask import Blueprint
from flask import request, jsonify, make_response
from api.manage_db import get_db, close_db
from api.nbp_data import YEARS, DATE_FORMAT
import datetime

rates = Blueprint('rates', __name__)

@rates.route('/api/rates/<date>', methods=['GET'])
def get_rate_for_day(date):
    cursor = get_db().cursor()
    if not validate_date(date):
         return jsonify({'message': 'Incorrect date format.'}), 400
    if (int(date.split('-')[0]) not in YEARS):
        return jsonify({'message': 'No data found for given date.'}), 404
    item = cursor.execute('SELECT rate, interpolated FROM rates WHERE date=?;', (date,)).fetchone()
    close_db()
    return jsonify({'date': date,'rate': item[0], 'interpolated': item[1]}), 200

@rates.route('/api/rates/<start_date>/<end_date>', methods=['GET'])
def get_rates_for_period(start_date, end_date):
    if not validate_date(start_date) or not validate_date(end_date) or not is_date_order_correct(start_date, end_date):
         return jsonify({'message': 'Incorrect date format.'}), 400
    cursor = get_db().cursor()
    if (int(start_date.split('-')[0]) not in YEARS or int(end_date.split('-')[0]) not in YEARS):
        return jsonify({'message': 'No data found for given date.'}), 404
    dates = get_dates_range(start_date, end_date)
    items = cursor.execute('SELECT * FROM rates WHERE date IN ({seq});'.format(seq=','.join(['?']*len(dates))), dates).fetchall()
    response = []
    for item in items:
        response.append({'date': item[0], 'rate': item[1], 'interpolated': item[2]})
    close_db()
    return jsonify({'rates': response})

@rates.route('/api/rates/last/<last>')
def get_last_rates(last):
    if int(last) < 0 or int(last) > 100:
        return jsonify({'message': 'Incorrect days amount. Maximum amount is 100.'}), 400
    cursor = get_db().cursor()
    items = cursor.execute('SELECT * FROM rates ORDER BY date DESC LIMIT ?;', (last,)).fetchall()
    response = []
    for item in items:
        response.append({'date': item[0], 'rate': item[1], 'interpolated': item[2]})
    close_db()
    return jsonify({'rates': response})
    
def validate_date(date_text):
    try:
        if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False
    
def is_date_order_correct(date_one, date_two):
    if datetime.datetime.strptime(date_one, "%Y-%m-%d") > datetime.datetime.strptime(date_two, "%Y-%m-%d"):
        return False
    return True

def get_dates_range(start_date, end_date):
    end = datetime.datetime.strptime(end_date, DATE_FORMAT)
    start = datetime.datetime.strptime(start_date, DATE_FORMAT)
    delta = end - start
    dates = []
    for i in range(delta.days + 1):
        dates.append((start + datetime.timedelta(days=i)).strftime(DATE_FORMAT))
    return dates