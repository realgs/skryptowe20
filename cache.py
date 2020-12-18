import constans
import schedule
import time
from db_handler import fetch_rates_for_period, fetch_sales_and_rates_for_period
from data_verifiers import to_datetime


rates = {}
rates_periods = []
sales = {}
sales_periods = []


def update_rates(start=constans.DB_START_DATE, end=constans.DB_END_DATE):
    rows = fetch_rates_for_period((start, end))
    for row in rows:
        rates[row[0]] = {'date': row[0], 'rate': row[1], 'interpolated': row[2]}

    rates_periods.append((to_datetime(start), to_datetime(end)))


def write_rate_to_cache(data):
    rates[data['date']] = data


def write_period_rates(data, start, end):
    for value in data:
        rates[value['date']] = value

    if not contains_period_rates((start, end)):
        rates_periods.append((to_datetime(start), to_datetime(end)))


def contains_period_rates(period):
    for per in rates_periods:
        if per[0] <= to_datetime(period[0]) and to_datetime(period[1]) <= per[1]:
            return True

    return False


def update_sales(start=constans.DB_START_DATE, end=constans.DB_END_DATE):
    rows = fetch_sales_and_rates_for_period((start, end))
    for row in rows:
        sales[row[0]] = {'date': row[0], 'rate': row[1], 'usd_sale': row[2], 'pln_sale': float(row[1]) * float(row[2])}

    sales_periods.append((to_datetime(start), to_datetime(end)))


def write_sale_to_cache(data):
    sales[data['date']] = data


def write_period_sales(data, start, end):
    for value in data:
        sales[value['date']] = value

    if not contains_period_sales((start, end)):
        sales_periods.append((to_datetime(start), to_datetime(end)))


def contains_period_sales(period):
    for per in sales_periods:
        if per[0] <= to_datetime(period[0]) and to_datetime(period[1]) <= per[1]:
            return True

    return False


def clear_cache():
    rates.clear()
    rates_periods.clear()
    sales.clear()
    sales_periods.clear()


def updates_manager(default_caching):
    if default_caching:
        schedule.every().day.at(constans.CACHE_UPDATE_TIME).do(update_rates)
        schedule.every().day.at(constans.CACHE_UPDATE_TIME).do(update_sales)
    else:
        schedule.every().day.at(constans.CACHE_UPDATE_TIME).do(clear_cache)

    while True:
        schedule.run_pending()
        time.sleep(1)
