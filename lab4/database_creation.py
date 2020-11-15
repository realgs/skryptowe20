import csv
import datetime as dt
import sqlite3 as sql
from currency_data import get_currency_rates
from typing import List
import config


def create_default_database(conn: sql.Connection):
    sql_create_table_customer = '''CREATE TABLE IF NOT EXISTS Customer (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    );'''

    sql_create_table_product = '''CREATE TABLE IF NOT EXISTS Item (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    );'''

    sql_create_table_order = '''CREATE TABLE IF NOT EXISTS SalesOrder (
                                        order_id text PRIMARY KEY,
                                        order_date date NOT NULL,
                                        customer_id text NOT NULL REFERENCES Customer (id),
                                        product_id text NOT NULL REFERENCES Item (id),
                                        quantity integer NOT NULL DEFAULT 1,
                                        sales real NOT NULL
                                    );'''
    if conn:
        create_table(conn, sql_create_table_customer)
        create_table(conn, sql_create_table_product)
        create_table(conn, sql_create_table_order)


def insert_default_data(conn: sql.Connection):
    csv_data = read_csv(config.CSV_FILE)[1:]

    products = set([(row[7], row[8]) for row in csv_data])

    customers = set([(row[3], row[4]) for row in csv_data])

    sales_orders = [
        (row[14],
         dt.datetime.strptime(str(row[9]), config.CSV_DATE_FORMAT).date().strftime(config.DATE_FORMAT),
         row[3],
         row[7],
         row[19],
         row[23]
         ) for row in csv_data]

    if conn:

        for product in products:
            insert_product(conn, product)

        for customer in customers:
            insert_customer(conn, customer)

        for sales_order in sales_orders:
            insert_order(conn, sales_order)


def create_table(con: sql.Connection, sql_create_table: str) -> bool:
    try:
        cursor = con.cursor()
        cursor.execute(sql_create_table)
        con.commit()
        return True
    except sql.Error as e:
        print(e)
    return False


def exec_sql(con: sql.Connection, execute_str: str, values) -> bool:
    try:
        cursor = con.cursor()
        cursor.execute(execute_str, values)
        con.commit()
        return True
    except sql.Error as e:
        print(e)
    return False


def insert_product(con: sql.Connection, product: (str, str)) -> bool:
    sql_exec = "INSERT INTO Item(id, name) VALUES(?, ?)"
    return exec_sql(con, sql_exec, product)


def insert_customer(con: sql.Connection, customer: (str, str)) -> bool:
    sql_exec = "INSERT INTO Customer(id, name) VALUES(?, ?)"
    return exec_sql(con, sql_exec, customer)


def insert_order(con: sql.Connection, sales_order: (int, str, str, str, str, int, float)) -> bool:
    sql_exec = '''INSERT INTO SalesOrder(order_id, order_date, customer_id,
                                    product_id, quantity, sales) VALUES(?,?,?,?,?,?)'''
    return exec_sql(con, sql_exec, sales_order)


def insert_rate(con: sql.Connection, currency_rates: (str, float)) -> bool:
    sql_exec = '''INSERT INTO CurrencyData(rating_date, rate) VALUES (?,?)'''
    return exec_sql(con, sql_exec, currency_rates)


def read_csv(csv_filepath: str, delimiter=';') -> List[List[str]]:
    with open(csv_filepath, newline='', encoding="utf8") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=delimiter)
        data = list(file_reader)
    return data


def create_currency_data_table(con: sql.Connection):
    if con:
        table_exec = '''CREATE TABLE IF NOT EXISTS CurrencyData (
                                            rating_date date NOT NULL,
                                            rate real NOT NULL
                                        );'''
        create_table(con, table_exec)


def fill_currency_table(con: sql.Connection):
    starting_date = dt.date(2013, 1, 1)
    end_date = dt.date(2016, 12, 31)
    delta = end_date - starting_date

    full_rates = [((starting_date + dt.timedelta(days=i)).strftime(config.DATE_FORMAT), None)
                  for i in range(delta.days + 1)]
    _, dates, rates = get_currency_rates('USD', delta.days, end_date)

    for date, rate in zip(dates, rates):
        if (date, None) in full_rates:
            full_rates[full_rates.index((date, None))] = (date, rate)

    if full_rates[0][1] is None:
        full_rates[0] = (full_rates[0][0], rates[0])

    for i in range(len(full_rates)):
        if full_rates[i][1] is None:
            full_rates[i] = (full_rates[i][0], full_rates[i - 1][1])
        insert_rate(con, full_rates[i])


if __name__ == '__main__':
    c = sql.connect(config.DATABASE_FILENAME)
    create_default_database(c)
    insert_default_data(c)
    create_currency_data_table(c)
    fill_currency_table(c)
    c.close()
