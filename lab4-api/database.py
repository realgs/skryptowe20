#!/bin/python3

import csv
import nbp
import config
import datetime as dt
import mysql.connector
from datetime import timedelta
from nbp import DATE_FORMAT, Currency
from typing import List, Optional, Tuple

CSV_FILE = "Superstore.csv"


def read_csv(csv_filepath: str, delimiter=';') -> List[List[str]]:
    data: List[List[str]] = []
    with open(csv_filepath, newline='', encoding="utf8") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=delimiter)
        data = list(file_reader)
    return data


def create_connection(config: dict) -> Optional[mysql.connector.MySQLConnection]:
    conn = None
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(err)
    return conn


def create_table(conn: mysql.connector.MySQLConnection, sql_create_table: str) -> bool:
    try:
        with conn.cursor() as c:
            c.execute(sql_create_table)
            conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err)
    return False


def create_product(conn:  mysql.connector.MySQLConnection, product: Tuple[str, str]) -> bool:
    sql = "INSERT INTO Product(id, name) VALUES(%s, %s)"
    try:
        with conn.cursor() as c:
            c.execute(sql, product)
            conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err)
    return False


def create_customer(conn:  mysql.connector.MySQLConnection, customer: Tuple[str, str]) -> bool:
    sql = "INSERT INTO Customer(id, name) VALUES(%s, %s)"
    try:
        c = conn.cursor()
        c.execute(sql, customer)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err)
    return False


def create_sales_order(conn:  mysql.connector.MySQLConnection, sales_order: Tuple[int, str,  str, str, str, float]) -> bool:
    sql = '''INSERT INTO SalesOrder(row_id, order_id, order_date, customer_id,
                                    product_id, sales) VALUES(%s,%s,%s,%s,%s,%s)'''
    try:
        with conn.cursor() as c:
            c.execute(sql, sales_order)
            conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err)
    return False


def create_default_database(conn:  mysql.connector.MySQLConnection):
    sql_create_table_customer = '''CREATE TABLE IF NOT EXISTS Customer (
                                        `id` varchar(15) PRIMARY KEY,
                                        `name` varchar(100) NOT NULL
                                    );'''

    sql_create_table_product = '''CREATE TABLE IF NOT EXISTS Product (
                                        `id` varchar(15) PRIMARY KEY,
                                        `name` varchar(300) NOT NULL
                                    );'''

    sql_create_table_order = '''CREATE TABLE IF NOT EXISTS SalesOrder (
                                        `row_id` int(11) PRIMARY KEY,
                                        `order_id` varchar(15) NOT NULL,
                                        `order_date` date NOT NULL,
                                        `customer_id` varchar(15) NOT NULL REFERENCES Customer (id),
                                        `product_id` varchar(15) NOT NULL REFERENCES Product (id),
                                        `sales` decimal(13,2) NOT NULL
                                    );'''

    csv_data = read_csv(CSV_FILE)[1:]

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
            create_sales_order(conn, sales_order)

# 3. Rozszerzyć bazę danych o tabelę, w której zawarta będzie informacja o średnich
# notowaniach tej waluty w stosunku do polskiej złotówki w wybranym przez siebie okresie
# (zależne od danych dostępnych w Waszej bazie danych) - niech to będą minimum 2 lata.
# Dni dla których nie podano notowań (takie jak weekendy) uzupełnić danymi z pierwszego dnia wstecz,
# dla którego jest wpisana wartość średniego kursu. Kod modyfikacji bazy zapisz również w repo.


def create_rate(conn:  mysql.connector.MySQLConnection, rate: Tuple[str, float]) -> bool:
    sql = "INSERT INTO UsdRatePln(rate_date, rate) VALUES(%s, %s)"
    try:
        with conn.cursor() as c:
            c.execute(sql, rate)
            conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err)
    return False


def add_rate_table_to_database(conn:  mysql.connector.MySQLConnection):
    sql_create_table_usd_rates_pln = '''CREATE TABLE IF NOT EXISTS UsdRatePln (
                                            `rate_date` date PRIMARY KEY,
                                            `rate` decimal(13,4) NOT NULL
                                        );'''
    create_table(conn, sql_create_table_usd_rates_pln)

    start_date = dt.date(2014, 1, 1)
    end_date = dt.date(2018, 1, 1)
    rates = nbp.rates_time_range(
        Currency.UNITED_STATES_DOLLAR, start_date, end_date, include_unrated_days=True)

    for rate in rates:
        create_rate(conn, (rate[1].strftime(DATE_FORMAT), rate[0]))


if __name__ == "__main__":
    conn = create_connection(config.mysql_config)
    if conn:
        create_default_database(conn)
        add_rate_table_to_database(conn)
        conn.close()
