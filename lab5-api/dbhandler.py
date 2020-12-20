import sqlite3
import datetime as dt
from enum import Enum
from config import DATABASE_FILE_PATH
from typing import Any, Dict, List, Tuple

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


currencyCodes = dict([(curr.code, curr) for curr in Currency])


def dict_factory(cursor: sqlite3.Cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def query_minmax_date() -> Tuple[dt.date, dt.date]:
    has_failed = False
    connection = None
    row = None
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        cursor = connection.cursor()
        row = cursor.execute(
            'SELECT MIN(date), MAX(date) FROM rates').fetchall()
        row = tuple([dt.datetime.strptime(date, DATE_FORMAT).date()
                     for date in row[0]])

    except sqlite3.Error as err:
        print(err)
        has_failed = True

    finally:
        if connection:
            connection.close()
        if has_failed:
            raise sqlite3.DatabaseError

    return row


def query_rates_range(currency: Currency, start_date: dt.date, end_date: dt.date, interpolated: bool = False) -> List[Dict[str, Any]]:
    pass


def query_rate(currency: Currency, date: dt.date, interpolated: bool = False) -> Dict[str, Any]:
    has_failed = False
    connection = None
    row = []
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        if interpolated:
            row = cursor.execute('SELECT * FROM rates WHERE date=? AND code=?',
                                 (date.strftime(DATE_FORMAT), currency.code)).fetchall()
        else:
            row = cursor.execute(
                'SELECT * FROM rates WHERE date=? AND code=? AND interpolated=0', (date.strftime(DATE_FORMAT), currency.code)).fetchall()

    except sqlite3.Error as err:
        print(err)
        has_failed = True

    finally:
        if connection:
            connection.close()
        if has_failed:
            raise sqlite3.DatabaseError

    if row:
        return row[0]
    return {}


def query_rates_all(currency: Currency, interpolated: bool = False) -> List[Dict[str, Any]]:
    has_failed = False
    connection = None
    rows = []
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        if interpolated:
            rows = cursor.execute('SELECT * FROM rates WHERE code=?',
                                  (currency.code,)).fetchall()
        else:
            rows = cursor.execute(
                'SELECT * FROM rates WHERE code=? AND interpolated=0', (currency.code,)).fetchall()

    except sqlite3.Error as err:
        print(err)
        has_failed = True

    finally:
        if connection:
            connection.close()
        if has_failed:
            raise sqlite3.DatabaseError

    return rows


def query_sales_sum(currency: Currency, date: dt.date) -> List[Dict[str, Any]]:
    pass
