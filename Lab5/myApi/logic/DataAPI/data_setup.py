from logic.DataAPI.fetcher import get_avg_rates_for_currency
from logic.DataAPI.database_operations import init_database
from logic.DataAPI.constants import SUMMARY_CURRENCIES, START_DATE, END_DATE

def setup():
    list_of_wrappers = []

    for c in SUMMARY_CURRENCIES:
        list_of_wrappers.append(get_avg_rates_for_currency(c, START_DATE, END_DATE))

    init_database(list_of_wrappers)
