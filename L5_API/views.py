from datetime import datetime
from L5_API import db_app
from L5_API.cache import RatesCache, SalesCache
from L5_API.constants import CURRENCIES, DATE_FORMAT, DATA_LIMIT

ratesCache = RatesCache()
salesCache = SalesCache()


def get_rates(code, date_from, date_to):
    if not _is_code(code):
        return '404 - Currency Code not found', 404

    are_dates_valid = _validate_dates(date_from, date_to, code)
    if not are_dates_valid[0]:
        return are_dates_valid[1], are_dates_valid[2]

    if ratesCache.is_cached_time_frame(date_from, date_to, code):
        data = ratesCache.get_cached(date_from, date_to, code)
    else:
        data = db_app.get_rates_ipd(code, date_from, date_to)
        ratesCache.cache(data, code)

    ratesCache.refresh()

    return _rates_serializer(code, data)


def get_rate(code, date):
    return get_rates(code, date, date)


def get_last_rate(code):
    limit = db_app.get_rates_limits(code)[1]
    return get_rates(code, limit, limit)


def get_sales(date_from, date_to):
    are_dates_valid = _validate_dates(date_from, date_to)
    if not are_dates_valid[0]:
        return are_dates_valid[1], are_dates_valid[2]

    if salesCache.is_cached_time_frame(date_from, date_to):
        data = salesCache.get_cached(date_from, date_to)
    else:
        data = db_app.get_sales(date_from, date_to)
        salesCache.cache(data)

    salesCache.refresh()

    return _sales_serializer(data)


def get_sale(date):
    return get_sales(date, date)


def get_rates_limits(code):
    if not _is_code(code):
        return '404 - Currency Code not found', 404

    date_min, date_max = db_app.get_rates_limits(code)
    return {"Currency Code": code.upper(), "Limits": {"Lower date limit": date_min, "Upper date limit": date_max}}


def get_sales_limits():
    date_min, date_max = db_app.get_sales_limits()
    return {"Sales": {"Lower date limit": date_min, "Upper date limit": date_max}}


def _sales_serializer(data):
    output = {"Sales": {}}
    for index, d in enumerate(data, start=1):
        output["Sales"][index] = {"Date": d["date"],
                                  "USD Total": d["total_usd"],
                                  "PLN Total": d["total_pln"]}
    return output


def _rates_serializer(code, data):
    output = {"Currency Code": code.upper(), "Rates": {}}
    for index, d in enumerate(data, start=1):
        output["Rates"][index] = {"Date": d["date"], "Rate": d["rate"], "Interpolated": d["ipd"]}
    return output


def _is_code(code):
    return code.upper() in CURRENCIES


def _are_dates(date_from, date_to):
    are_dates = True

    try:
        datetime.strptime(date_from, DATE_FORMAT)
        datetime.strptime(date_to, DATE_FORMAT)
    except ValueError:
        are_dates = False

    return are_dates


def _are_dates_chronological(date_from, date_to):
    return date_from <= date_to


def _are_in_limit(date_from, date_to, code):
    if code == 'NONE':
        date_min, date_max = db_app.get_sales_limits()
    else:
        date_min, date_max = db_app.get_rates_limits(code)

    date_min = datetime.strptime(date_min, DATE_FORMAT).date()
    date_max = datetime.strptime(date_max, DATE_FORMAT).date()

    return date_min <= date_to <= date_max and date_min <= date_from <= date_max


def _are_in_range(date_from, date_to):
    return (date_to - date_from).days < DATA_LIMIT


def _validate_dates(date_from, date_to, code='NONE'):
    if not _are_dates(date_from, date_to):
        return False, '400 BadRequest - Wrong format of dates - should be 0000-00-00', 400

    date_from = datetime.strptime(date_from, DATE_FORMAT).date()
    date_to = datetime.strptime(date_to, DATE_FORMAT).date()

    if not _are_dates_chronological(date_from, date_to):
        return False, '400 BadRequest - Invalid date range - endDate is before startDate', 400

    if not _are_in_limit(date_from, date_to, code):
        return False, '400 BadRequest - Invalid date range - date outside the database limit', 400

    if not _are_in_range(date_from, date_to):
        return False, '400 BadRequest - Limit of {} days has been exceeded'.format(DATA_LIMIT), 400

    return True, '', 200


def _validate_date(date, code='NONE'):
    return _validate_dates(date, date, code)
