import sqlite3

DB_NAME = 'data.db'


def create_exchange_rates_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS rates(date text, rate real)''')
    conn.commit()
    conn.close()


def populate_exchange_rates_table(rates_and_dates):
    if len(rates_and_dates) < 1:
        print("Incorrect data")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO rates VALUES (?, ?)", rates_and_dates)
    conn.commit()
    conn.close()

def drop_exchange_rates_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''DROP TABLE IF EXISTS rates''')
    conn.commit()
    conn.close()
