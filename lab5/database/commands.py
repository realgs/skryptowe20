from .connection import connect
from datetime import date


def insert_into_pln_currencies(currency):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO purchasing.pln_currencies(currency_date, currency_value, interpolated) VALUES(%s, %s, %s)", currency)


def get_currencies_in_range(date_from: date, date_to: date):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM purchasing.pln_currencies WHERE currency_date >= '{date_from}' AND currency_date <= '{date_to}'")
        return cursor.fetchall()

