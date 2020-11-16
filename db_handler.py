import sqlite3
import pandas as pd
from sqlite3 import Error

DB_FILE = 'database.db'
CSV_FILE = 'sales_data_sample.csv'


def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
    except Error as e:
        print(e)

    return conn


def insert_csv_data():
    conn = connect_to_db()
    df = pd.read_csv(CSV_FILE)
    df.to_sql('sales_data', conn, if_exists='replace', index=False)
    conn.close()


def create_rates_table():
    conn = connect_to_db()
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS avg_rates (
                                                day date, 
                                                rate real
                                                )''')
        conn.close()
    except Error as e:
        print(e)


def insert_values_to_rates_table(values):
    conn = connect_to_db()
    c = conn.cursor()
    c.executemany('''INSERT INTO avg_rates(day, rate) VALUES (?, ?)''', values)
    conn.commit()
    conn.close()


def get_sums_and_rates_for_dates(dates):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute(f'''SELECT ORDERDATE, SUM(SALES), rate
                  FROM sales_data
                  INNER JOIN avg_rates ON ORDERDATE = day
                  GROUP BY ORDERDATE
                  HAVING ORDERDATE IN {tuple(dates)}
                  ORDER BY ORDERDATE
                ''')
    rows = c.fetchall()
    conn.close()
    return rows


def get_first_sale_date():
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''SELECT MIN(ORDERDATE)
                 FROM sales_data''')
    values = c.fetchall()
    conn.close()
    return values
