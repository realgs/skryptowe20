import sqlite3
import datetime as dt
from enum import Enum
from typing import Any, Dict, List

DATE_FORMAT = "%Y-%m-%d"


class Currency(Enum):
    UNITED_STATES_DOLLAR = "USD"
    THAI_BAHT = "THB"
    AUSTRALIAN_DOLLAR = "AUD"
    HONG_KONG_DOLLAR = "HKD"
    CANADIAN_DOLLAR = "CAD"
    NEW_ZEALAND_DOLLAR = "NZD"
    EUROPEAN_EURO = "EUR"
    POLISH_ZLOTY = "PLN"
    JAPANESE_YEN = "JPY"
    BRITISH_POUND = "GBP"
    SWISS_FRANC = "CHF"

    def __init__(self, code: str) -> None:
        self.code = code

    @property
    def title(self) -> str:
        return self.name.lower().replace('_', ' ')


def query_rates_range(currency: Currency, start_date: dt.date, end_date: dt.date) -> List[Dict[str, Any]]:
    pass


def query_rate(currency: Currency, date: dt.date) -> Dict[str, Any]:
    pass


def query_rates_all(currency: Currency) -> List[Dict[str, Any]]:
    pass


def query_sales_sum(currency: Currency, date: dt.date) -> List[Dict[str, Any]]:
    pass
