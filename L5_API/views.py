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
    return __rates_serializer(code, rates)


def get_sales(date_from, date_to):
    if __are_dates(date_from, date_to):
        return '400 BadRequest - Wrong format of dates - should be 0000-00-00', 400

    date_from, date_to = __valid_dates(date_from, date_to)
    sales = db_app.get_sales(date_from, date_to)
    return __sales_serializer(sales)


def __sales_serializer(data):
    output = {"Sales": {}}
    for index, d in enumerate(data, start=1):
        output["Sales"][index] = {"Date": d["date"],
                                                 "USD Total": d["total_usd"],
                                                 "PLN Total": d["total_pln"]}
    return output


def __rates_serializer(code, data):
    output = {"Currencycode": code.upper(), "Rates": {}}
    for index, d in enumerate(data, start=1):
        output["Rates"][index] = {"Date": d["date"], "Rate": d["rate"], "Interpolated": d["ipd"]}
    return output


def __is_code(code):
    return code in CURRENCIES


def __is_date(date):
    is_date = True

    try:
        datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        is_date = False

    return is_date


def __are_dates(date_from, date_to):
    are_dates = True

    try:
        datetime.strptime(date_from, DATE_FORMAT)
        datetime.strptime(date_to, DATE_FORMAT)
    except ValueError:
        are_dates = False

    return are_dates


def __valid_dates(date_from, date_to, code='NONE'):
    date_from = datetime.strptime(date_from, DATE_FORMAT).date()
    date_to = datetime.strptime(date_to, DATE_FORMAT).date()

    if code == 'NONE':
        date_min, date_max = db_app.get_sales_limits()
    else:
        date_min, date_max = db_app.get_rates_limits(code)

    date_min = datetime.strptime(date_min, DATE_FORMAT).date()
    date_max = datetime.strptime(date_max, DATE_FORMAT).date()

    # date_from = max(date_from, date_min)
    # date_to = min(date_to, date_max)

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
