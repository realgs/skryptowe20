from enum import Enum
from os.path import isfile, dirname, join
from datetime import datetime, timedelta
import sqlite3

from .data_creation import (
    DB_CUSTOM_DATE_FORMAT,
    create_or_update_currency_table,
    create_or_update_sales_tables,
)


DB_FILE = "BikeStores.db"
PATH_TO_DATABASE = join(dirname(__file__), DB_FILE)


class Currency(Enum):
    USD = "USD"
    EURO = "EUR"


class DatabaseLimits:
    def __init__(self):
        self.min_rates_date = self.max_rates_date = None
        self.min_sales_date = self.max_sales_date = None

    def load_limits(self, connection):
        cursor = connection.cursor()

        min_date, max_date = cursor.execute(
            "SELECT MIN(date), MAX(date) FROM pln_rates"
        ).fetchone()

        self.min_rates_date = datetime.strptime(min_date, DB_CUSTOM_DATE_FORMAT).date()
        self.max_rates_date = datetime.strptime(max_date, DB_CUSTOM_DATE_FORMAT).date()

        min_date, max_date = cursor.execute(
            "SELECT MIN(date), MAX(date) FROM total_sales"
        ).fetchone()

        self.min_sales_date = datetime.strptime(min_date, DB_CUSTOM_DATE_FORMAT).date()
        self.max_sales_date = datetime.strptime(max_date, DB_CUSTOM_DATE_FORMAT).date()


def check_if_database_file_exists(file_=PATH_TO_DATABASE):
    if not isfile(file_):
        raise FileNotFoundError(f"File {file_} does not exist.")


def update_data():
    check_if_database_file_exists()
    connection = sqlite3.connect(PATH_TO_DATABASE)
    create_or_update_currency_table(connection, Currency.USD)
    create_or_update_sales_tables(connection)
    connection.close()

    connection.close()


def get_rates_for_dates(connection, from_date, to_date):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT date, rate, interpolated
        FROM pln_rates
        WHERE date BETWEEN ? AND ?
        ORDER BY date
        """,
        (
            from_date.strftime(DB_CUSTOM_DATE_FORMAT),
            to_date.strftime(DB_CUSTOM_DATE_FORMAT),
        ),
    )

    rates = [
        {
            "date": datetime.strptime(date.split(" ")[0], DB_CUSTOM_DATE_FORMAT).date(),
            "rate": rate,
            "interpolated": bool(ord(interpolated)),
        }
        for date, rate, interpolated in cursor
    ]

    return rates


def add_day_with_no_sales(sales, date):
    sales.append(
        {
            "date": date,
            "original_total": 0,
            "exchanged_total": 0,
        }
    )


def add_days_until(sales, from_date, to_date):
    while from_date != to_date:
        add_day_with_no_sales(sales, from_date)
        from_date = from_date + timedelta(days=1)
    return from_date


def get_sales_for_dates(connection, from_date, to_date):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT date, original_sales, exchanged_sales
        FROM total_sales
        WHERE date BETWEEN ? AND ?
        ORDER BY date
        """,
        (
            from_date.strftime(DB_CUSTOM_DATE_FORMAT),
            to_date.strftime(DB_CUSTOM_DATE_FORMAT),
        ),
    )

    sales = []
    for date, original, exchanged in cursor:
        date = datetime.strptime(date.split(" ")[0], DB_CUSTOM_DATE_FORMAT).date()

        from_date = add_days_until(sales, from_date, date)

        from_date = from_date + timedelta(days=1)
        sales.append(
            {
                "date": date,
                "original_total": original,
                "exchanged_total": exchanged,
            }
        )

    if not sales:
        add_days_until(sales, from_date, to_date)

    return sales
