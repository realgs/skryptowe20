import sqlite3
from sqlite3 import Error
from flask import g
import flask
import pandas
from datetime import date
from lab5_solutions.utils import MAX_DATE, MIN_DATE, DATE_FORMAT
from lab5_solutions.nbp_api import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")

# DATABASE_PATH = '.\database.db'
TABLE_NAME = 'exchange_rates'
CREATE_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS exchange_rates (
                                               currency TEXT NOT NULL,
                                               date DATE NOT NULL,
                                               rate REAL NOT NULL,
                                               interpolated INTEGER NOT NULL,
                                               PRIMARY KEY (currency, date)
                                           ); '''

DROP_TABLE_QUERY = 'DROP TABLE IF EXISTS {}'


def get_database():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def create_table():
    try:
        cursor = get_database().cursor()
        cursor.execute(CREATE_TABLE_QUERY)
    except Error as e:
        print(e)


def fill_table_period(start_date, end_date, currency):
    rates = get_avg_rates_from_period(currency, start_date, end_date)
    missed_dates = pandas.date_range(start_date, end_date)
    rates_df = pandas.DataFrame(rates)
    rates_df.set_index('date', inplace=True)
    rates_df.index = pandas.DatetimeIndex(rates_df.index)
    rates_df = rates_df.reindex(index=missed_dates, method='ffill')
    rates_df.fillna(inplace=True, method='bfill')
    rates_df.index = rates_df.index.strftime(DATE_FORMAT)

    cursor = get_database().cursor()
    for day in rates_df.to_records():
        interpolated = 1
        for x in rates:
            if x['date'] == day[0]:
                interpolated = 0

        tuple = (currency.value, day[0], day[1], interpolated)
        cursor.execute('INSERT OR IGNORE INTO exchange_rates VALUES (?,?,?,?)', tuple)

    cursor.connection.commit()


def drop_table(table_name):
    cursor = get_database().cursor()
    cursor.execute(DROP_TABLE_QUERY.format(table_name))


def select_rate_one_day(currency, date):
    cursor = get_database().cursor()
    cursor.execute(
        """
        SELECT currency, date, rate, interpolated
        FROM exchange_rates 
        WHERE DATE(date) IS DATE('{}') AND currency = '{}'
        """.format(date, currency)
    )
    return [{'currency': x[0], 'date': x[1], 'rate': x[2], 'interpolated': True if x[3] == 1 else False} for x in
            cursor.fetchall()]


def select_rate_between_dates(currency, start_date, end_date):
    cursor = get_database().cursor()
    cursor.execute(
        """
        SELECT currency, date, rate, interpolated
        FROM exchange_rates 
        WHERE (DATE(date) BETWEEN DATE('{}') AND DATE('{}')) AND currency = '{}'
        ORDER BY date
        """.format(start_date, end_date, currency)
    )
    return [{'currency': x[0], 'date': x[1], 'rate': x[2], 'interpolated': True if x[3] == 1 else False} for x in
            cursor.fetchall()]


def get_sale_in_USD_PLN_one_day(currency, date):
    cursor = get_database().cursor()
    cursor.execute(
        """
        SELECT order_date 'SaleDate', SUM(sales) 'Currency', ROUND(SUM(sales) * rate, 2) 'PLN'
        FROM SalesOrder, exchange_rates 
        WHERE DATE(order_date) IS '{}'
        AND DATE(order_date) = DATE(date) AND currency = '{}'
        GROUP BY order_date
        """.format(date, currency)
    )

    return [{'date': x[0], currency: x[1], 'pln': x[2]} for x in
            cursor.fetchall()]


def get_sale_in_USD_PLN_from_date_to_date(currency, start_date, end_date):
    cursor = get_database().cursor()
    cursor.execute(
        """
        SELECT order_date 'SaleDate', SUM(sales) 'Currency', ROUND(SUM(sales) * rate, 2) 'PLN'
        FROM SalesOrder, exchange_rates 
        WHERE (DATE(order_date) BETWEEN '{}' AND '{}')
        AND DATE(order_date) = DATE(date) AND currency = '{}'
        GROUP BY order_date
        """.format(start_date, end_date, currency)
    )

    return [{'date': x[0], currency: x[1], 'pln': x[2]} for x in
            cursor.fetchall()]


if __name__ == '__main__':
    app = flask.Flask(__name__)
    with app.app_context():
        drop_table(TABLE_NAME)
        create_table()
        start_date = MIN_DATE
        end_date = MAX_DATE
        fill_table_period(start_date, end_date, Currency.USD)
        fill_table_period(start_date, end_date, Currency.EUR)
        close_connection(get_database().cursor().connection)
