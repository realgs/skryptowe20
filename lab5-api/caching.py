import datetime as dt
from typing import Dict

import dbhandler
from dbhandler import Currency, DATE_FORMAT


def cache_sales_sum_original() -> Dict[dt.date, float]:
    cached: Dict[dt.date, float] = {}
    sales_summed = dbhandler.query_sales_sum_all_original()
    for row in sales_summed:
        cached[dt.datetime.strptime(
            row['date'], DATE_FORMAT).date()] = round(float(row['sum']), 2)
    return cached


def cache_sales_sum_exchanged(currency: Currency) -> Dict[dt.date, Dict[str, float]]:
    cached: Dict[dt.date, Dict[str, float]] = {}
    sales_summed = dbhandler.query_sales_sum_all_exchanged(currency)
    for row in sales_summed:
        cached[dt.datetime.strptime(
            row['date'], DATE_FORMAT).date()] = {'sum': round(float(row['sum']), 2), 'rate': float(row['rate'])}
    return cached


if __name__ == "__main__":
    print(cache_sales_sum_original())
    # print(cache_sales_sum_exchanged(Currency.UNITED_STATES_DOLLAR))
    pass
