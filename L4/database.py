#!/usr/bin/python3

import sqlite3
import currency_API

def connect_and_get_cursor(database_name):
    connention = sqlite3.connect(database_name)
    return connention.cursor()

def get_available_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()

def get_table(cursor, table_name):
    cursor.execute("SELECT * FROM " + table_name + ";")
    return cursor.fetchall()

def table_exists(cursor, table_name):
    return (table_name,) in get_available_tables(cursor)

def clear_table(cursor, table_name):
    if table_exists(cursor, table_name):
        cursor.execute("DELETE FROM " + table_name + ";")

def drop_table(cursor, table_name):
    if table_exists(cursor, table_name):
        cursor.execute("DROP TABLE " + table_name + ";")

def assure_table(cursor, table_name, table_body):
    print('available tables:', get_available_tables(cursor))

    if not table_exists(cursor, table_name):
        cursor.execute(table_body)

        if table_exists(cursor, table_name):
            print('table', table_name, 'defined')
        else:
            print('failed to define', table_name)

    print('available tables:', get_available_tables(cursor))

def assure_markings(cursor):
    markings_body = \
    '''
        CREATE TABLE markings
        (
            exchange_date DATE PRIMARY KEY,
            mid_price REAL NOT NULL
        );
    '''
    assure_table(cursor, 'markings', markings_body)

def insert_into_markings(cursor, markings_dictionary):
    insert_body = "INSERT INTO markings (exchange_date, mid_price) VALUES\n"

    for date in markings_dictionary.keys():
        insert_body += "('" + date.strftime("%Y-%m-%d") + "', " + str(markings_dictionary[date]) + "),\n"

    insert_body = insert_body[:-2] + ";"
    cursor.execute(insert_body)

def select_sales_data(cursor, date_from, date_to):
    select_body = "\
        SELECT exchange_date, IFNULL(mid_price * SUM(sales), 0), IFNULL(SUM(sales), ) \
        FROM markings LEFT JOIN SalesOrder \
        ON markings.exchange_date = SalesOrder.order_date \
        WHERE markings.exchange_date BETWEEN '" + date_from.strftime("%Y-%m-%d") + "' AND '" + date_to.strftime("%Y-%m-%d") + \
        "' GROUP BY order_date, mid_price; ORDER BY exchange_date"

    cursor.execute(select_body)

    return cursor.fetchall()

def refill_markings(cursor, currency_code, database_from, database_to):
    assure_markings(cursor)
    clear_table(cursor, 'markings')
    database_markings = currency_API.get_currency_markings_from_date_range(currency_code, database_from, database_to)
    insert_into_markings(cursor, database_markings)
