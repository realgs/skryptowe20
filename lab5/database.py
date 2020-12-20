import sqlite3
import nbp_requests

DATABASE_NAME = "database.db"


def connect():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(e)

    return connection


def drop_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS UsdPlnExchangeRate')


def create_exchange_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UsdPlnExchangeRate(
            RateId INTEGER PRIMARY KEY ASC,
            RateDate DATETIME NOT NULL,
            Exchange REAL NOT NULL,
            Interpolated BIT NOT NULL
        )''')


def fill_table(cursor, start_date, end_date):
    usd_exchange_rates = nbp_requests.get_currency_between_dates(nbp_requests.US_DOLLAR, start_date, end_date)
    for rate in usd_exchange_rates:
        cursor.execute('INSERT INTO UsdPlnExchangeRate VALUES(NULL, ?,?,?)', (rate[0], rate[1], rate[2]))


if __name__ == '__main__':
    conn = connect()
    cursor = conn.cursor()
    drop_table(cursor)
    create_exchange_table(cursor)
    fill_table(cursor, '2018-07-04', '2020-05-06')
    conn.commit()
    conn.close()
