#!/bin/python3

import csv
import nbp
import lzma
import sqlite3
import datetime as dt
from datetime import timedelta
from nbp import DATE_FORMAT, Currency
from typing import List, Optional, Tuple

DATABASE_FILE = "database.sqlite"
CSV_XZ_FILE = "Superstore.csv.xz"


def read_csv_xz(csv_xz_filepath: str, delimiter=';') -> List[List[str]]:
    data: List[List[str]] = []
    with lzma.open(csv_xz_filepath) as csvfile:
        text: List[str] = [str(line, encoding='utf8')
                           for line in csvfile.readlines()]
        file_reader = csv.reader(text, delimiter=delimiter)
        data = list(file_reader)
    return data


def create_connection(db_filepath: str) -> Optional[sqlite3.Connection]:
    conn = None
    try:
        conn = sqlite3.connect(db_filepath)
    except sqlite3.Error as err:
        print(err)
    return conn


def create_table(conn: sqlite3.Connection, sql_create_table: str) -> bool:
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_product(conn: sqlite3.Connection, product: Tuple[str, str]) -> bool:
    sql = "INSERT INTO Products(id, name) VALUES(?, ?)"
    try:
        c = conn.cursor()
        c.execute(sql, product)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_customer(conn: sqlite3.Connection, customer: Tuple[str, str]) -> bool:
    sql = "INSERT INTO Customers(id, name) VALUES(?, ?)"
    try:
        c = conn.cursor()
        c.execute(sql, customer)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_order(conn: sqlite3.Connection, sales_order: Tuple[int, str,  str, str, str, float]) -> bool:
    sql = '''INSERT INTO Orders(row_id, order_id, order_date, customer_id,
                                    product_id, value) VALUES(?,?,?,?,?,?)'''
    try:
        c = conn.cursor()
        c.execute(sql, sales_order)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_default_database(conn: sqlite3.Connection):
    sql_create_table_customer = '''CREATE TABLE IF NOT EXISTS Customers (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    );'''

    sql_create_table_product = '''CREATE TABLE IF NOT EXISTS Products (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    );'''

    sql_create_table_order = '''CREATE TABLE IF NOT EXISTS Orders (
                                        row_id integer PRIMARY KEY,
                                        order_id text NOT NULL,
                                        order_date date NOT NULL,
                                        customer_id text NOT NULL,
                                        product_id text NOT NULL,
                                        value real NOT NULL,
                                        FOREIGN KEY (customer_id) REFERENCES Customer (id),
                                        FOREIGN KEY (product_id) REFERENCES Product (id)
                                    );'''

    csv_data = read_csv_xz(CSV_XZ_FILE)[1:]

    products = set([(row[13], row[16]) for row in csv_data])

    customers = set([(row[5], row[6]) for row in csv_data])

    sales_orders = [(int(row[0]), row[1], dt.datetime.strptime(row[2], "%d.%m.%Y").date().strftime(
        DATE_FORMAT), row[5], row[13], float(row[17].replace(",", "."))) for row in csv_data]

    if conn:
        create_table(conn, sql_create_table_customer)
        create_table(conn, sql_create_table_product)
        create_table(conn, sql_create_table_order)

        for product in products:
            create_product(conn, product)

        for customer in customers:
            create_customer(conn, customer)

        for sales_order in sales_orders:
            create_order(conn, sales_order)


def create_currency(conn: sqlite3.Connection, curr: Tuple[str]) -> bool:
    sql = '''INSERT INTO Currencies(code) VALUES(?)'''
    try:
        c = conn.cursor()
        c.execute(sql, curr)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_rate(conn: sqlite3.Connection, rate: Tuple[str, str, float, bool]) -> bool:
    sql = "INSERT INTO Rates(code, date, rate, interpolated) VALUES(?, ?, ?, ?)"
    try:
        c = conn.cursor()
        c.execute(sql, rate)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def add_rate_table_to_database(conn: sqlite3.Connection):
    sql_create_table_currency = '''CREATE TABLE IF NOT EXISTS Currencies (
                                            code text PRIMARY KEY
                                        );'''

    sql_create_rates = '''CREATE TABLE IF NOT EXISTS Rates (
                                            code text NOT NULL,
                                            date NOT NULL,
                                            rate real NOT NULL,
                                            interpolated BOOLEAN NOT NULL CHECK (interpolated IN (0,1)),
                                            FOREIGN KEY (code) REFERENCES Currencies (code),
                                            PRIMARY KEY (code, date)
                                        );'''

    create_table(conn, sql_create_table_currency)
    create_table(conn, sql_create_rates)


def add_rates_to_database(conn: sqlite3.Connection, currency: nbp.Currency):
    start_date = dt.date(2010, 1, 3)
    end_date = dt.datetime.now().date()

    rates = nbp.rates_time_range(
        currency, start_date, end_date, include_unrated_days=False)

    rates_normal = [(date, rate, False) for rate, date in rates]

    rates_set = set(rates)

    rates_inter_set = set(nbp.rates_time_range(
        currency, start_date, end_date, include_unrated_days=True))

    rates_inter = [(date, rate, True) for rate,
                   date in rates_inter_set.difference(rates_set)]

    rates_normal.extend(rates_inter)
    for rate in rates_normal:
        create_rate(conn, (currency.code, rate[0].strftime(
            DATE_FORMAT), rate[1], rate[2]))


if __name__ == "__main__":
    conn = create_connection(DATABASE_FILE)
    if conn:
        create_default_database(conn)
        add_rate_table_to_database(conn)
        for currency in nbp.Currency:
            if currency != nbp.Currency.POLISH_ZLOTY:
                create_currency(conn, (currency.code,))
                add_rates_to_database(conn, currency)
        conn.close()
