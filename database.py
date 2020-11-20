from datetime import datetime, timedelta
import sqlite3
import json
from nbp import fetch_currency_from_two_tables, from_json_to_list


DB_NAME = "Source/bazunia.db"
DATEFORMAT = "%Y-%m-%d"
TIME_DELTA = 182


def create_avg_currency_rates_table(conn):
    c = conn.cursor()
    c.execute(
    '''
    CREATE TABLE if not exists AvgUsdRates (
        avg_rates REAL NOT NULL,
        date DATE PRIMARY KEY NOT NULL
    )
    '''
    )
    conn.commit()


def insert_usd_rates(conn, rates):
    c = conn.cursor()
    c.executemany('INSERT INTO AvgUsdRates VALUES (?, ?)', rates)
    conn.commit()


def add_missing_dates(rates):
    for i in range(len(rates) - 1):
        curr = rates[i]
        next = rates[i + 1]

        curr_date = datetime.strptime(curr[1], DATEFORMAT)
        next_date = datetime.strptime(next[1], DATEFORMAT)
        delta = next_date - curr_date

        if delta.days > 1:
            next_day = curr_date + timedelta(days=1)
            rates.insert(i + 1, (
                curr[0],
                next_day.strftime(DATEFORMAT)
            ))
    return rates


def update_dates(conn, years):
    c = conn.cursor()
    c.execute(
        f'''
        UPDATE Orders
        SET OrderDate = DATETIME(OrderDate, '+{years} YEARS')
        '''
    )


def get_sales_usd_pln(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT
        '''
    )

if __name__ == "__main__":
    conn = sqlite3.connect(DB_NAME)
    conn.text_factory = bytes

    # DB OPERATIONS
    # rates = from_json_to_list(fetch_avg_currency(days=TIME_DELTA))
    # new_rates = add_missing_dates(rates)

    create_avg_currency_rates_table(conn)
    # insert_usd_rates(conn, rates)

    update_dates(conn, 15)
    c = conn.cursor()
    c.execute(''' SELECT MAX(OrderDate) FROM Orders''')
    print(c.fetchall(), sep='\n')

    conn.close()
