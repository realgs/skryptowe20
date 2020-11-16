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
