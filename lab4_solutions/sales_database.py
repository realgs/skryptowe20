from sqlite3 import Error, connect

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas

from currency import Currency
from exceptions import ArgumentException
from task1 import *

DATABASE_PATH = '.\database.db'
TABLE_NAME = 'exchange_rates'
CREATE_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS exchange_rates (
                                               date DATE PRIMARY KEY,
                                               rate REAL NOT NULL
                                           ); '''

INSERT_DATA_QUERY = 'INSERT INTO exchange_rates(date,rate) VALUES({},{})'
DROP_TABLE_QUERY = 'DROP TABLE {}'
DATE_FORMAT = "%Y-%m-%d"


def connect_to_database(db_file):
    connection = None
    try:
        connection = connect(db_file)
    except Error as e:
        print(e)
    return connection


def create_table(connection):
    try:
        c = connection.cursor()
        c.execute(CREATE_TABLE_QUERY)
    except Error as e:
        print(e)


def fill_table_period(connection, start_date, end_date, currency: Currency):
    rates = average_quotation_rates(currency.value, start_date, end_date)
    missed_dates = pandas.date_range(start_date, end_date)
    rates_df = pandas.DataFrame(rates)
    rates_df.set_index('date', inplace=True)
    rates_df.index = pandas.DatetimeIndex(rates_df.index)
    rates_df = rates_df.reindex(index=missed_dates, method='ffill')
    rates_df.fillna(inplace=True, method='bfill')
    rates_df.index = rates_df.index.strftime(DATE_FORMAT)
    cur = connection.cursor()
    for day in rates_df.to_records():
        cur.execute(
            '''
                   INSERT INTO exchange_rates VALUES (?,?)
                ON CONFLICT(date) DO NOTHING
                ''', day)

    connection.commit()


def fill_table_last_x_rates(connection, number_of_last_days, currency: Currency):
    if number_of_last_days < 0:
        raise ArgumentException('Cannot take negative number of days: {}'.format(number_of_last_days))

    start_day = date.today() - timedelta(number_of_last_days - 1)
    end_day = date.today()
    fill_table_period(connection, start_day, end_day, currency)


def _drop_table(connection, table_name):
    cursor = connection.cursor()
    dropTableStatement = DROP_TABLE_QUERY.format(table_name)
    cursor.execute(dropTableStatement)


def close_connection(connection):
    connection.close()


def create_sales(connection, start_date, end_date):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT order_date 'SaleDate', SUM(sales) 'USD', SUM(sales) * rate 'PLN'
        FROM SalesOrder, exchange_rates 
        WHERE (DATE(order_date) BETWEEN '{}' AND '{}')
        AND DATE(order_date) = DATE(date)
        GROUP BY order_date
        """.format(start_date, end_date)
    )

    result = cursor.fetchall()
    dates = []
    usd = []
    pln = []
    for res in result:
        dates.append(res[0])
        usd.append(res[1])
        pln.append(res[2])

    fig, axs = plt.subplots(figsize=(12, 4))

    axs.plot(dates, usd, 'b-', label='USD')
    axs.plot(dates, pln, 'g-', label='PLN')

    axs.xaxis.set_major_locator(ticker.MaxNLocator(25))

    plt.gcf().autofmt_xdate(rotation=30)
    fig.tight_layout()
    plt.title('My first graph!')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    conn = connect(DATABASE_PATH)
    _drop_table(conn, TABLE_NAME)
    create_table(conn)
    end_date = date(2016, 12, 28)
    start_date = end_date - timedelta(days=365 * 2 + 1)
    fill_table_period(conn, start_date, end_date, Currency.USD)
    create_sales(conn, start_date, end_date)
    close_connection(conn)
