import sqlite3
import functions

DATABASE_NAME = "database.db"


def connect():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(e)

    return connection


def get_prices_in_year():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''SELECT 
                    orderDate,
                    SUM(UnitPrice * Quantity*(1-Discount)) AS UsdPrice,
                    MAX(RateDate) AS RateDate, 
                    Exchange,
                    SUM(UnitPrice * Quantity*(1-Discount)) * Exchange AS PlnPrice
                    FROM "Order Details" NATURAL JOIN Orders JOIN UsdPlnExchangeRate ON OrderDate >= rateDate
                    WHERE OrderDate>="2019-05-06"
                    GROUP BY OrderDate''')
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def drop_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS UsdPlnExchangeRate')


def create_exchange_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UsdPlnExchangeRate(
            RateId INTEGER PRIMARY KEY ASC,
            RateDate DATETIME NOT NULL,
            Exchange REAL NOT NULL
        )''')


def fill_table(cursor, start_date, end_date):
    usd_exchange_rates = functions.get_currency_between_dates(functions.US_DOLLAR, start_date, end_date)
    for rate in usd_exchange_rates:
        cursor.execute('INSERT INTO UsdPlnExchangeRate VALUES(NULL, ?,?)', (rate[0], rate[1]))


if __name__ == '__main__':
    conn = connect()
    cursor = conn.cursor()
    drop_table(cursor)
    create_exchange_table(cursor)
    # zad 4
    fill_table(cursor, '2018-05-06', '2020-05-06')
    conn.commit()
    conn.close()
