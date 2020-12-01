import datetime
import sqlite3
import exchange_rates_api

DATA_BASE_FILE = "sales_data.db"


def create_exchange_rate_table():
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE ExchangeRates (exchange_date date PRIMARY KEY, exchange_rate real NOT NULL);")
    conn.close()


def insert_exchange_rates(exchange_rates_dict):
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    for (date, rate) in exchange_rates_dict.items():
        cursor.execute("INSERT INTO ExchangeRates VALUES ('" + str(date) + "', " + str(rate) +");")
    conn.commit()
    conn.close()


def get_sales_data(first_day, last_day):
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT ExchangeRates.exchange_date, IFNULL(SUM(SalesOrder.sales),0), ExchangeRates.exchange_rate * IFNULL(SUM(SalesOrder.sales),0) \
FROM ExchangeRates LEFT JOIN SalesOrder \
ON ExchangeRates.exchange_date = SalesOrder.order_date \
GROUP BY ExchangeRates.exchange_date, ExchangeRates.exchange_rate \
HAVING ExchangeRates.exchange_date BETWEEN '" + str(first_day) + "' AND '" + str(last_day) + "';")
    sales_data = []
    for (date, sales, sales_pln) in cursor.fetchall():
        sales_data.append((exchange_rates_api.str_to_date(date), sales, sales_pln))
    conn.close()
    return sales_data
