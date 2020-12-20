from datetime import datetime
from L5_API import db_app
from L5_API.constants import CURRENCIES, DATE_FORMAT, DATA_LIMIT


def get_last_date(code):
    return {"Date": db_app.get_last_date(code)}


def get_last_rate(code):
    date = db_app.get_last_date(code)
    rate, ipd = db_app.get_rate(code, date)
    return {"Currencycode": code, "Rates": {"Rate": {"Date": date, "Rate": rate, "Interpolated": ipd}}}


def get_sale(date):
    is_date_valid = __test_date(date)
    if not is_date_valid[0]:
        return is_date_valid[1], is_date_valid[2]

    sales = db_app.get_sales(date, date)
    return __sales_serializer(sales)


def get_rates(code, date_from, date_to):
    are_dates_valid = __test_dates(date_from, date_to, code)
    if not are_dates_valid[0]:
        return are_dates_valid[1], are_dates_valid[2]

    rates = db_app.get_rates_ipd(code, date_from, date_to)
    return __rates_serializer(code, rates)


def get_sales(date_from, date_to):
    are_dates_valid = __test_dates(date_from, date_to)
    if not are_dates_valid[0]:
        return are_dates_valid[1], are_dates_valid[2]

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


def __are_dates_chronological(date_from, date_to):
    return date_from < date_to


def __are_in_range(date_from, date_to, code):
    if code == 'NONE':
        date_min, date_max = db_app.get_sales_limits()
    else:
        date_min, date_max = db_app.get_rates_limits(code)

    date_min = datetime.strptime(date_min, DATE_FORMAT).date()
    date_max = datetime.strptime(date_max, DATE_FORMAT).date()

    return date_to > date_min or date_to < date_max or date_from > date_min or date_from < date_max


def __are_in_limit(date_from, date_to):
    return (date_to - date_from).days < DATA_LIMIT


def __test_date(date, code='NONE'):
    if not __is_date(date):
        return False, '400 BadRequest - Wrong format of date - should be 0000-00-00', 400

    date = datetime.strptime(date, DATE_FORMAT).date()

    if not __are_in_range(date, date, code):
        return False, '400 BadRequest - Invalid date range - date outside the database limit', 400

    return True, '', 200


def __test_dates(date_from, date_to, code='NONE'):
    if not __are_dates(date_from, date_to):
        return False, '400 BadRequest - Wrong format of dates - should be 0000-00-00', 400

    date_from = datetime.strptime(date_from, DATE_FORMAT).date()
    date_to = datetime.strptime(date_to, DATE_FORMAT).date()

    if not __are_dates_chronological(date_from, date_to):
        return False, '400 BadRequest - Invalid date range - endDate is before startDate', 400

    if not __are_in_range(date_from, date_to, code):
        return False, '400 BadRequest - Invalid date range - date outside the database limit', 400

    if not __are_in_limit(date_from, date_to):
        return False, '400 BadRequest - Limit of {} days has been exceeded'.format(DATA_LIMIT), 400

    return True, '', 200
