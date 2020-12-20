from typing import Dict
import datetime as dt
from dbhandler import Currency


def cache_sales_sum_original() -> Dict[dt.date, float]:
    pass


def cache_sales_sum(currency: Currency, original_cached: Dict[dt.date, float]) -> Dict[dt.date, float]:
    pass
