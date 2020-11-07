#!/bin/python3

import csv
from datetime import timedelta
import sqlite3
from typing import List, Optional, Tuple
import datetime as dt
from nbp import DATE_FORMAT, Currency
import nbp

DATABASE_FILE = "database.db"
CSV_FILE = "Superstore.csv"


def read_csv(csv_filepath: str) -> List[List[str]]:
    data: List[List[str]] = []
    with open(csv_filepath, newline='', encoding="utf8") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=';')
        for row in file_reader:
            data.append(row)
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
    sql = "INSERT INTO Product(id, name) VALUES(?, ?)"
    try:
        c = conn.cursor()
        c.execute(sql, product)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_customer(conn: sqlite3.Connection, customer: Tuple[str, str]) -> bool:
    sql = "INSERT INTO Customer(id, name) VALUES(?, ?)"
    try:
        c = conn.cursor()
        c.execute(sql, customer)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_sales_order(conn: sqlite3.Connection, sales_order: Tuple[int, str,  str, str, str, float]) -> bool:
    sql = '''INSERT INTO SalesOrder(row_id, order_id, order_date, customer_id,
                                    product_id, sales) VALUES(?,?,?,?,?,?)'''
    try:
        c = conn.cursor()
        c.execute(sql, sales_order)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def create_default_database():
    sql_create_table_customer = '''CREATE TABLE IF NOT EXISTS Customer (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    );'''

    sql_create_table_product = '''CREATE TABLE IF NOT EXISTS Product (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    );'''

    sql_create_table_order = '''CREATE TABLE IF NOT EXISTS SalesOrder (
                                        row_id integer PRIMARY KEY,
                                        order_id text NOT NULL,
                                        order_date date NOT NULL,
                                        customer_id text NOT NULL REFERENCES Customer (id),
                                        product_id text NOT NULL REFERENCES Product (id),
                                        sales real NOT NULL
                                    );'''

    csv_data = read_csv(CSV_FILE)[1:]

    products = set([(row[13], row[16]) for row in csv_data])

    customers = set([(row[5], row[6]) for row in csv_data])

    sales_orders = [(int(row[0]), row[1], dt.datetime.strptime(row[2], "%d.%m.%Y").date().strftime(
        DATE_FORMAT), row[5], row[13], float(row[17].replace(",", "."))) for row in csv_data]

    conn = create_connection(DATABASE_FILE)
    if conn:
        create_table(conn, sql_create_table_customer)
        create_table(conn, sql_create_table_product)
        create_table(conn, sql_create_table_order)

        for product in products:
            create_product(conn, product)

        for customer in customers:
            create_customer(conn, customer)

        for sales_order in sales_orders:
            create_sales_order(conn, sales_order)

        conn.close()

# 3. Rozszerzyć bazę danych o tabelę, w której zawarta będzie informacja o średnich
# notowaniach tej waluty w stosunku do polskiej złotówki w wybranym przez siebie okresie
# (zależne od danych dostępnych w Waszej bazie danych) - niech to będą minimum 2 lata.
# Dni dla których nie podano notowań (takie jak weekendy) uzupełnić danymi z pierwszego dnia wstecz,
# dla którego jest wpisana wartość średniego kursu. Kod modyfikacji bazy zapisz również w repo.


def create_rate(conn: sqlite3.Connection, rate: Tuple[str, float]) -> bool:
    sql = "INSERT INTO UsdRatesPln(rate_date, rate) VALUES(?, ?)"
    try:
        c = conn.cursor()
        c.execute(sql, rate)
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(err)
    return False


def add_rates_table_to_database(conn: sqlite3.Connection):
    sql_create_table_usd_rates_pln = '''CREATE TABLE IF NOT EXISTS UsdRatesPln (
                                            rate_date date NOT NULL,
                                            rate real NOT NULL,
                                            PRIMARY KEY (rate_date, rate)
                                        );'''
    create_table(conn, sql_create_table_usd_rates_pln)

    usd = Currency.UNITED_STATES_DOLLAR
    rates = nbp.rates_time_range(usd, dt.datetime(
        2014, 1, 1), dt.datetime(2017, 12, 31))

    # fill gaps in rates
    tmp_rates: List[Tuple[float, dt.date]] = []
    for index, rate in enumerate(rates[:-1]):
        days_difference = (rates[index + 1][1] - rate[1]).days
        if days_difference > 1:
            tmp_date = rate[1]
            for _ in range(days_difference):
                tmp_date = tmp_date + timedelta(days=1)
                tmp_rates.append((rate[0], tmp_date))
    rates.extend(tmp_rates)

    for rate in rates:
        create_rate(conn, (rate[1].strftime(DATE_FORMAT), rate[0]))


if __name__ == "__main__":
    # create_default_database()
    conn = create_connection(DATABASE_FILE)
    c = conn.cursor()
    # c.execute("DELETE FROM UsdRatesPln")
    # conn.commit()

    # with open("output.txt", "w") as f:
    #     for row in rows:
    #         f.write(f'{" ".join(row)}\n')

    add_rates_table_to_database(conn)
