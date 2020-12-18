from db_operations import get_rates_for_dates
from constans import START_DATE, END_DATE, to_datetime

rates_cache = {}
sales_cache = {}
requests_cache = []


def update_cache():
    data_rates = get_rates_for_dates(START_DATE, END_DATE)

    for date, rate, interpolated in data_rates:
        rates_cache[date] = {'date': date, 'usd_rate': rate, 'interpolated': interpolated}

    requests_cache.clear()
    sales_cache.clear()


def has_rate(date_string):
    return date_string in rates_cache


def has_rate_range(date_start, date_end):
    return [key for key in rates_cache.keys() if date_start <= to_datetime(key) <= date_end]


def has_request(date_range):
    return date_range in requests_cache, date_range


def get_rates_from_range(dates):
    response = {}
    for key in dates:
        response[key] = rates_cache[key]
    return response


def has_sale(date_string):
    return date_string in sales_cache


def get_sales_from_range(date_range):
    date_start, date_end = date_range
    response = {}
    dates = [key for key in sales_cache.keys() if date_start <= to_datetime(key) <= date_end]
    for key in dates:
        response[key] = sales_cache[key]
    return response
