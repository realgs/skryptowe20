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
    has_failed = False
    connection = None
    rows = []
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        if interpolated:
            rows = cursor.execute('SELECT * FROM rates WHERE date BETWEEN ? AND ? AND code=?;',
                                  (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT), currency.code)).fetchall()
        else:
            rows = cursor.execute(
                'SELECT * FROM rates WHERE date BETWEEN ? AND ? AND code=? AND interpolated=0;',
                (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT), currency.code)).fetchall()

    except sqlite3.Error as err:
        print(err)
        has_failed = True

    finally:
        if connection:
            connection.close()
        if has_failed:
            raise sqlite3.DatabaseError

    return rows


def query_rate(currency: Currency, date: dt.date, interpolated: bool = False) -> Dict[str, Any]:
    has_failed = False
    connection = None
    row = []
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        if interpolated:
            row = cursor.execute('SELECT * FROM rates WHERE date=? AND code=?;',
                                 (date.strftime(DATE_FORMAT), currency.code)).fetchall()
        else:
            row = cursor.execute(
                'SELECT * FROM rates WHERE date=? AND code=? AND interpolated=0;', (date.strftime(DATE_FORMAT), currency.code)).fetchall()

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
            rows = cursor.execute('SELECT * FROM rates WHERE code=?;',
                                  (currency.code,)).fetchall()
        else:
            rows = cursor.execute(
                'SELECT * FROM rates WHERE code=? AND interpolated=0;', (currency.code,)).fetchall()

    except sqlite3.Error as err:
        print(err)
        has_failed = True

    finally:
        if connection:
            connection.close()
        if has_failed:
            raise sqlite3.DatabaseError

    return rows


def query_sales_sum_all_original() -> List[Dict[str, Any]]:
    has_failed = False
    connection = None
    rows = []
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        rows = cursor.execute(
            'SELECT order_date"date", SUM(value)"sum" FROM orders GROUP BY order_date').fetchall()

    except sqlite3.Error as err:
        print(err)
        has_failed = True

    finally:
        if connection:
            connection.close()
        if has_failed:
            raise sqlite3.DatabaseError

    return rows


def query_sales_sum_all_exchanged(currency: Currency) -> List[Dict[str, Any]]:
    has_failed = False
    connection = None
    rows = []
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        rows = cursor.execute(
            '''SELECT O.order_date"date", SUM(O.value)*R.rate"sum" 
               FROM orders O JOIN rates R ON O.order_date=R.date AND R.code=?
               GROUP BY order_date;''', (currency.code,)).fetchall()

    except sqlite3.Error as err:
        print(err)
        has_failed = True

    finally:
        if connection:
            connection.close()
        if has_failed:
            raise sqlite3.DatabaseError

    return rows


if __name__ == "__main__":
    # print(query_minmax_date())
    # print(query_rates_all(Currency.EUROPEAN_EURO, interpolated=True))
    # print(query_rate(Currency.UNITED_STATES_DOLLAR, dt.date(2011,1,1), interpolated=True))
    # print(query_sales_sum_all_original())
    # print(query_sales_sum_all_exchanged(Currency.UNITED_STATES_DOLLAR))
    pass
