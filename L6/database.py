#!/usr/bin/python3

import sqlite3
import currency_API

DATABASE_NAME = "sales_data.db"


def get_available_tables():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    connection.close()
    return tables

def get_table(table_name):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table_name + ";")
    table = cursor.fetchall()
    connection.close()
    return table

def get_limited_table(table_name, top_count):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table_name + " ORDER BY exchange_date DESC LIMIT " + str(top_count) + ";")
    table = cursor.fetchall()
    connection.close()
    return table

def table_exists(table_name):
    return (table_name,) in get_available_tables()

def clear_table(table_name):
    if table_exists(table_name):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM " + table_name + ";")
        connection.commit()
        connection.close()

def drop_table(table_name):
    if table_exists(table_name):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE " + table_name + ";")
        connection.commit()
        connection.close()

def assure_table(table_name, table_body):
    print('available tables:', get_available_tables())

    if not table_exists(table_name):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute(table_body)

        if table_exists(table_name):
            print('table', table_name, 'defined')
        else:
            print('failed to define', table_name)

        print('available tables:', get_available_tables())
        connection.close()

def assure_markings():
    markings_body = \
    '''
        CREATE TABLE markings
        (
            exchange_date DATE PRIMARY KEY,
            mid_price REAL NOT NULL,
            currency_code VARCHAR NOT NULL,
            interpolated BOOLEAN NOT NULL CHECK (interpolated IN (0, 1))
        );
    '''
    assure_table('markings', markings_body)

def insert_into_markings(markings_dictionary, currency_code='USD'):
    insert_body = "INSERT INTO markings (exchange_date, mid_price, currency_code, interpolated) VALUES\n"

    for date in markings_dictionary.keys():
        insert_body += "('" + date.strftime("%Y-%m-%d") + "', " + str(markings_dictionary[date][0]) + ", '" + currency_code + "', " + str(markings_dictionary[date][1]) + "),\n"

    insert_body = insert_body[:-2] + ";"
    print(insert_body)
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(insert_body)
    connection.commit()
    connection.close()

def select_sales_data(date_from, date_to):
    select_body = "\
        SELECT exchange_date, IFNULL(mid_price * SUM(sales), 0), IFNULL(SUM(sales), 0) \
        FROM SalesOrder LEFT JOIN markings \
        ON markings.exchange_date = SalesOrder.order_date \
        WHERE SalesOrder.order_date BETWEEN '" + date_from.strftime("%Y-%m-%d") + "' AND '" + date_to.strftime("%Y-%m-%d") + \
        "' GROUP BY order_date, mid_price ORDER BY exchange_date;"

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(select_body)
    sales_data = cursor.fetchall()
    connection.close()
    return sales_data

def get_sales_from_period(date_from, date_to):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    sales_data = []

    select_body = "\
        SELECT order_date, IFNULL(SUM(sales), 0) \
        FROM SalesOrder \
        WHERE order_date BETWEEN '" + date_from.strftime("%Y-%m-%d") + "' AND '" + date_to.strftime("%Y-%m-%d") + \
        "' GROUP BY order_date ORDER BY order_date;"
    cursor.execute(select_body)
    sales = cursor.fetchall()
    for sales_item in sales:
        sales_data += [{ 'date' : sales_item[0], 'PLN' : sales_item[1] }]

    for (currency_code, ) in get_available_currencies():
        select_body = "\
            SELECT exchange_date, IFNULL(mid_price * SUM(sales), 0) \
            FROM SalesOrder LEFT JOIN markings \
            ON markings.exchange_date = SalesOrder.order_date \
            WHERE currency_code = '" + currency_code + "' AND SalesOrder.order_date BETWEEN '" + date_from.strftime("%Y-%m-%d") + "' AND '" + date_to.strftime("%Y-%m-%d") + \
            "' GROUP BY order_date, mid_price ORDER BY exchange_date;"
        cursor.execute(select_body)
        sales = cursor.fetchall()
        for i in range(len(sales)):
            sales_data[i][currency_code] = sales[i][1]

    connection.close()
    return sales_data

def get_daily_sales(date):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    select_body = "\
        SELECT order_date, IFNULL(SUM(sales), 0) \
        FROM SalesOrder WHERE order_date = '" + date.strftime("%Y-%m-%d") + \
        "' GROUP BY order_date ORDER BY order_date;"
    cursor.execute(select_body)
    sales = cursor.fetchall()

    if sales:
        sales_data = { 'date' : sales[0][0], 'PLN' : sales[0][1] }

        for (currency_code, ) in get_available_currencies():
            select_body = "\
                SELECT exchange_date, IFNULL(mid_price * SUM(sales), 0) \
                FROM SalesOrder LEFT JOIN markings \
                ON markings.exchange_date = SalesOrder.order_date \
                WHERE currency_code = '" + currency_code + "' AND SalesOrder.order_date = '" + date.strftime("%Y-%m-%d") + \
                "' GROUP BY order_date, mid_price ORDER BY order_date;"
            cursor.execute(select_body)
            sales = cursor.fetchall()
            if sales: sales_data[currency_code] = sales[0][1]
            else: sales_data[currency_code] = 0

        connection.close()
        return sales_data

    else: return { 'date' : date.strftime("%Y-%m-%d"), 'PLN' : 0 }

def refill_markings(currency_code, database_from, database_to):
    assure_markings()
    clear_table('markings')
    database_markings = currency_API.get_currency_markings_from_date_range(currency_code, database_from, database_to)
    insert_into_markings(database_markings, currency_code)

def get_oldest_marking_date(currency_code=''):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    if currency_code:
        cursor.execute("SELECT MIN(exchange_date) FROM markings WHERE currency_code='" + currency_code + "';")
    else:
        cursor.execute("SELECT MIN(exchange_date) FROM markings;")

    date = cursor.fetchall()[0][0]
    connection.close()
    return date

def get_newest_marking_date(currency_code=''):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    if currency_code:
        cursor.execute("SELECT MAX(exchange_date) FROM markings WHERE currency_code='" + currency_code + "';")
    else:
        cursor.execute("SELECT MAX(exchange_date) FROM markings;")

    date = cursor.fetchall()[0][0]
    connection.close()
    return date

def get_oldest_sale_date():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT MIN(order_date) FROM SalesOrder;")
    date = cursor.fetchall()[0][0]
    connection.close()
    return date

def get_newest_sale_date():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(order_date) FROM SalesOrder;")
    date = cursor.fetchall()[0][0]
    connection.close()
    return date

def get_all_daily_markings(date):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM markings WHERE exchange_date ='" + date.strftime("%Y-%m-%d") + "';")
    markings = cursor.fetchall()
    connection.close()
    return markings

def get_all_currency_markings(currency_code):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM markings WHERE currency_code = '" + currency_code + "';")
    markings = cursor.fetchall()
    connection.close()
    return markings

def get_limited_currency_markings(currency_code, top_count):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM markings WHERE currency_code = '" + currency_code + "' ORDER BY exchange_date DESC LIMIT " + str(top_count) + ";")
    table = cursor.fetchall()
    connection.close()
    return table

def get_currency_daily_markings(currency_code, date):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM markings WHERE exchange_date ='" + date.strftime("%Y-%m-%d") + "' AND currency_code = '" + currency_code + "';")
    markings = cursor.fetchall()
    connection.close()
    return markings

def get_available_currencies():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT currency_code FROM markings;")
    currency_list = cursor.fetchall()
    connection.close()
    return currency_list

def check_currency_availability(currency_code):
    currency_list = get_available_currencies()
    return (currency_code.upper(),) in currency_list

def get_markings_from_period(date_from, date_to):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM markings WHERE exchange_date BETWEEN '" + date_from.strftime("%Y-%m-%d") + "' AND '" + date_to.strftime("%Y-%m-%d") + "';")
    markings = cursor.fetchall()
    connection.close()
    return markings

def get_currency_markings_from_period(currency_code, date_from, date_to):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM markings WHERE currency_code = '" + currency_code + "' AND exchange_date BETWEEN '" + date_from.strftime("%Y-%m-%d") + "' AND '" + date_to.strftime("%Y-%m-%d") + "';")
    markings = cursor.fetchall()
    connection.close()
    return markings


if __name__ == "__main__":
    print(check_currency_availability("USD"))
    print(get_oldest_marking_date("USD"))
    print(get_oldest_marking_date())
    # print(get_table("markings"))
