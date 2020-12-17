import constans
import schedule
import time
from db_handler import get_avg_rates_table, get_sums_and_rates_for_period

rates_cache = {}
sales_cache = {}


def update_rates_cache():
    rows = get_avg_rates_table()
    for row in rows:
        rates_cache[row[0]] = {'rate': row[1], 'interpolated': row[2]}


def update_sales_cache():
    rows = get_sums_and_rates_for_period((constans.DB_START_DATE, constans.DB_END_DATE))
    for row in rows:
        sales_cache[row[0]] = {'rate': row[1], 'usd_sum': row[2], 'pln_sum': float(row[1]) * float(row[2])}


def updates_manager():
    schedule.every().day.at(constans.CACHE_UPDATE_TIME).do(update_rates_cache)
    schedule.every().day.at(constans.CACHE_UPDATE_TIME).do(update_sales_cache)

    while True:
        schedule.run_pending()
        time.sleep(1)
