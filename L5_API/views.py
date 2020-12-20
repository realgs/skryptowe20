from datetime import datetime, timedelta

from flask import jsonify
from L5_API import db_app
from L5_API.constants import CURRENCIES, DATE_FORMAT, DATA_LIMIT


def get_last_date(code):
    return jsonify(date=db_app.get_last_date(code))


def get_last_rate(code):
    date = db_app.get_last_date(code)
    rate, ipd = db_app.get_rate(code, date)
    return {"Currencycode": code, "Rates": {"Rate": {"Date": date, "Rate": rate, "Interpolated": ipd}}}


def get_rates(code, date_from, date_to):
    if __are_dates(date_from, date_to):
        date_from, date_to = __valid_dates(date_from, date_to, code)
        rates = db_app.get_rates_ipd(code, date_from, date_to)
    else:
        rates = []
    return __serializer(code, rates)


def __serializer(code, data):
    output = {"Currencycode": code.upper(), "Rates": {}}
    for index, d in enumerate(data, start=1):
        output["Rates"]["Rate" + str(index)] = {"Date": d["date"], "Rate": d["rate"], "Interpolated": d["ipd"]}
    return output


def __is_code(code):
    return code in CURRENCIES


def __is_date(date):
    return date == datetime.strptime(date, DATE_FORMAT).strftime(DATE_FORMAT)


def __are_dates(date_from, date_to):
    return __is_date(date_from), __is_date(date_to)


def __valid_dates(date_from, date_to, code):
    error_msg = ''

    date_from = datetime.strptime(date_from, DATE_FORMAT).date()
    date_to = datetime.strptime(date_to, DATE_FORMAT).date()
    date_min, date_max = db_app.get_limits(code)
    date_min = datetime.strptime(date_min, DATE_FORMAT).date()
    date_max = datetime.strptime(date_max, DATE_FORMAT).date()

    if (date_to - date_from).days > DATA_LIMIT:
        print('400 BadRequest - Limit of {} days has been exceeded\n'.format(DATA_LIMIT))
        date_from = date_to - timedelta(days=DATA_LIMIT)

    if date_from > date_to:
        print('400 BadRequest - Invalid date range - endDate is before startDate\n')
        date_temp = date_to
        date_to = date_from
        date_from = date_temp

    if date_from < date_min:
        print('400 BadRequest - Invalid date range - startDate outside the db limit\n')
        date_from = date_min
    elif date_from > date_max:
        print('400 BadRequest - Invalid date range - startDate outside the db limit\n')
        date_from = date_max - timedelta(days=1)

    if date_to < date_min:
        print('400 BadRequest - Invalid date range - endDate outside the db limit\n')
        date_to = date_min + timedelta(days=1)
    elif date_from > date_max:
        print('400 BadRequest - Invalid date range - endDate outside the db limit\n')
        date_to = date_max

    return date_from, date_to
