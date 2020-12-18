import sqlite3
import constants as const
from sqlite3 import Error


def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect(const.DB_FILE)
    except Error as e:
        print(e)

    return conn


def create_rates_table():
    conn = connect_to_db()
    try:
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS  avg_rates''')
        c.execute('''CREATE TABLE IF NOT EXISTS avg_rates (
                                                day date, 
                                                rate real,
                                                interpolated boolean
                                                )''')
        conn.close()
    except Error as e:
        print(e)


def insert_values_to_rates_table(values):
    conn = connect_to_db()
    c = conn.cursor()
    c.executemany('''INSERT INTO avg_rates(day, rate, interpolated) VALUES (?, ?, ?)''', values)
    conn.commit()
    conn.close()


def fetch_rates_for_period(period):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''SELECT day, rate, interpolated
                 FROM avg_rates
                 WHERE day BETWEEN ? AND ?
                 ORDER BY day
                ''', period)
    rows = c.fetchall()
    conn.close()
    return rows


def fetch_rate_for_date(date):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''SELECT day, rate, interpolated
                 FROM avg_rates
                 WHERE day = ?
                ''', (date, ))
    row = c.fetchall()
    conn.close()
    return row


def fetch_sales_and_rates_for_period(period):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''SELECT ORDERDATE, rate, SUM(SALES)
                 FROM sales_data
                 INNER JOIN avg_rates ON ORDERDATE = day
                 WHERE ORDERDATE BETWEEN ? AND ?
                 GROUP BY ORDERDATE
                 ORDER BY ORDERDATE
                ''', period)
    rows = c.fetchall()
    conn.close()
    return rows


def fetch_sale_and_rate_for_date(date):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''SELECT orderdate, rate, SUM(sales)
                 FROM sales_data
                 INNER JOIN avg_rates ON orderdate = day
                 WHERE orderdate = ?
                 GROUP BY orderdate''', (date, ))
    row = c.fetchall()
    conn.close()
    return row


def fetch_first_sale_date():
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''SELECT MIN(ORDERDATE)
                 FROM sales_data''')
    values = c.fetchall()
    conn.close()
    return values
