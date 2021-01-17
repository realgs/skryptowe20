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


def currencies_table_empty() -> bool:
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT CASE WHEN EXISTS (SELECT * FROM purchasing.pln_currencies LIMIT 1) THEN 1 ELSE 0 END")
        return not bool(cursor.fetchall())


def get_sales_for_date(request_date: date):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT \"USD\", \"PLN\" FROM purchasing.sales WHERE duedate = '{request_date}'")
        return cursor.fetchall()

def get_sales_in_range(date_from: date, date_to: date):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT \"duedate\", \"USD\", \"PLN\" FROM purchasing.sales WHERE duedate >= '{date_from}' AND duedate <= '{date_to}'")
        return cursor.fetchall()