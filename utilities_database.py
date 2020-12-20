import os
import pandas as pd
import sqlite3 as sql
from datetime import datetime
from utilities_nbp import call_nbp_api_for


DATE_COL = "DateRecorded"
SALES_TABLE_NAME = "sales"
RATES_TABLE_TEMPLATE = "{}_exchange_rate_table"
COLUMNS_TO_DROP = ["ID", "SerialNumber", "ListYear", "NonUseCode", "Remarks"]
DB_PATH = os.path.join(os.path.dirname(__file__), "my_db.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "real-estate-sales-2001-2017-1.csv")
FIRST_DAY_OF_NBP_CURRENCY_RATE = "2002-01-02"
TABLE_A = ["usd", "eur", "huf", "chf", "gbp", "jpy", "czk"]
TABLE_B = ["aed", "bob"]
TODAY = lambda: datetime.now().strftime('%Y-%m-%d')


def create_database():
    """
    Creates database with available exchange rates for all supported 
    currencies and with sales data from .csv file.

    Args:
        from_date (datetime.date): first day of period
        till_date (datetime.date): last days of period
    """
    if os.path.isfile(DB_PATH):
        conn = sql.connect(DB_PATH)
    else:
        conn = init_database_from_csv()
    for code in TABLE_A:
        add_currency_table(conn, code, "a")
    for code in TABLE_B:
        add_currency_table(conn, code, "b")
    conn.commit()
    conn.close()


def init_database_from_csv():
    """
    Chooses only important data from .csv sales file and inserts it into database.

    Returns:
        sqlite3.Connection: conection to database
    """
    sales = pd.read_csv(CSV_PATH).dropna()
    sales = sales.infer_objects()
    sales[DATE_COL] = pd.to_datetime(
        sales[DATE_COL], errors="coerce", infer_datetime_format=True)
    sales[DATE_COL] = sales[DATE_COL].astype(str)
    sales = sales.drop(columns=COLUMNS_TO_DROP)
    conn = sql.connect(DB_PATH)
    sales.to_sql(SALES_TABLE_NAME, conn)
    return conn


def add_currency_table(conn, code, table, from_date=FIRST_DAY_OF_NBP_CURRENCY_RATE):
    """
    Adds exchange rates of given currency from period between from_date 
    and till_date to database.

    Args:
        conn (sqlite3.Connection): conection to database
        code (str): code of currency
        table (str): name of table
        from_date (str): first day of period
    """
    c = conn.cursor()
    actual_table = RATES_TABLE_TEMPLATE.format(code)
    c.execute(f'DROP TABLE IF EXISTS {actual_table}')
    c.execute(f'CREATE TABLE {actual_table} (date TEXT, rate REAL, interpolated INTEGER)')
    insert_exchange_rates_to_database(conn, code, table, from_date, TODAY())


def update_datebase():
    """
    Updates exchange rates from missing days in database.
    """
    conn = sql.connect(DB_PATH)
    select_cmd = "SELECT max(date) FROM " + RATES_TABLE_TEMPLATE.format("usd")
    c = conn.cursor()
    c.execute(select_cmd)
    last_saved_day = c.fetchall()[0][0]
    actual_day = TODAY()
    for code in TABLE_A:
        insert_exchange_rates_to_database(conn, code, "a", last_saved_day, actual_day)
    for code in TABLE_B:
        insert_exchange_rates_to_database(conn, code, "b", last_saved_day, actual_day)
    conn.commit()
    conn.close()


def insert_exchange_rates_to_database(conn, code, table, from_date, till_date):
    """
    Inserts data from NBP Api to database.

    Args:
        conn (sqlite3.Connection): conection to database
        code (str): code of currency
        table (str): name of table
        from_date (datetime.date): first day of period
        till_date (datetime.date): last days of period
    """
    curr_table = RATES_TABLE_TEMPLATE.format(code)
    exchange_data = call_nbp_api_for(code, table, from_date=from_date, till_date=till_date)
    (dates, (rates_and_interpolated)) = zip(*exchange_data.items())
    rates, interpolates = zip(*rates_and_interpolated)
    interpolates = list(map(int, interpolates))
    exchange_data = [(x, y, z) for x, y, z in zip(dates, rates, interpolates)]
    conn.cursor().executemany(f'INSERT INTO {curr_table} VALUES (?,?,?)', exchange_data)
