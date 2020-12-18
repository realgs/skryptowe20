import sqlite3

import nbp_operations

from constans import DB_NAME, START_DATE, END_DATE


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as err:
        print(err)
    return conn

def create_rates_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS rates(rate_dates data PRIMARY KEY NOT NULL, rate REAL, interpolated BOOLEAN)''')
    conn.commit()
    conn.close()


def insert_rates(rate_vals_interpolated):
    if len(rate_vals_interpolated) < 1:
        print("Incorrect data")
        return
    conn = create_connection()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO rates VALUES (?, ?, ?)", rate_vals_interpolated)
    conn.commit()
    conn.close()




def get_sales_sum_for_dates(start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    interval = (start_date, end_date)
    sales_data = cursor.execute(
        f'''SELECT SUM(sales), orderdate, rate
            FROM sales_table
            JOIN rates ON orderdate = rate_dates
            WHERE rate_dates BETWEEN ? AND ?
            GROUP BY orderdate''', interval).fetchall()
    conn.close()

    return sales_data


def get_rates_for_dates(start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    interval = (start_date, end_date)
    rates_data = cursor.execute(
        f'''SELECT rate_dates, rate, interpolated
            FROM rates
            WHERE rate_dates BETWEEN ? AND ?
          ''', interval).fetchall()
    conn.close()

    return rates_data


def get_sales_sum_for_day(day):
    conn = create_connection()
    cursor = conn.cursor()
    sales_data = cursor.execute(
        f'''SELECT SUM(sales), orderdate, rate
            FROM sales_table
            JOIN rates ON orderdate = rate_dates
            WHERE rate_dates = '{day}'
            GROUP BY orderdate''').fetchall()
    conn.close()

    return sales_data


def get_rates_for_day(day):
    conn = create_connection()
    cursor = conn.cursor()
    rates_data = cursor.execute(
        f'''SELECT rate_dates, rate, interpolated
            FROM rates
            WHERE rate_dates = '{day}'
          ''').fetchall()
    conn.close()

    return rates_data


def drop_rate_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS rates")
    conn.close()


def db_init():
    drop_rate_table()
    create_rates_table()
    vals = nbp_operations.request_between_dates('usd', START_DATE, END_DATE)
    insert_rates(vals)
