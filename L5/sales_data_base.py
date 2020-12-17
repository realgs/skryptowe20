import datetime
import sqlite3

DATA_BASE_FILE = "sales_data.db"

def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def create_exchange_rate_table():
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE ExchangeRates (exchange_date date PRIMARY KEY, exchange_rate real NOT NULL, \
        interpolated BOOLEAN NOT NULL CHECK (interpolated IN (0,1)) );")
    conn.close()


def insert_exchange_rates(exchange_rates_intepolated_dict):
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    for (date, (rate, interpolated)) in exchange_rates_intepolated_dict.items():
        cursor.execute("INSERT INTO ExchangeRates VALUES ('" + str(date) + "', " + str(rate) + ", " + ("1" if interpolated else "0") + ");")
    conn.commit()
    conn.close()


def get_sales_data(first_day, last_day):
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall()
    cursor.execute("SELECT ExchangeRates.exchange_date, IFNULL(SUM(SalesOrder.sales),0), ExchangeRates.exchange_rate * IFNULL(SUM(SalesOrder.sales),0) \
FROM ExchangeRates LEFT JOIN SalesOrder \
ON ExchangeRates.exchange_date = SalesOrder.order_date \
GROUP BY ExchangeRates.exchange_date, ExchangeRates.exchange_rate \
HAVING ExchangeRates.exchange_date BETWEEN '" + str(first_day) + "' AND '" + str(last_day) + "';")
    sales_data = []
    for (date, sales, sales_pln) in cursor.fetchall():
        sales_data.append((str_to_date(date), sales, sales_pln))
    conn.close()
    return sales_data


def get_exchange_rates_data(first_day, last_day):
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall()
    cursor.execute("SELECT ExchangeRates.exchange_date, ExchangeRates.exchange_rate, ExchangeRates.interpolated \
FROM ExchangeRates \
WHERE ExchangeRates.exchange_date BETWEEN '" + str(first_day) + "' AND '" + str(last_day) + "';")
    rates_data = []
    for (date, rate, interpolated) in cursor.fetchall():
        rates_data.append({'date': date, 'rate': rate, 'interpolated': True if interpolated == 1 else False})
    conn.close()
    return rates_data


def get_first_last_day_rates_data():
    conn = sqlite3.connect(DATA_BASE_FILE)
    cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall()
    cursor.execute("SELECT MIN(ExchangeRates.exchange_date), MAX(ExchangeRates.exchange_date) \
    FROM ExchangeRates")
    fetch_data = cursor.fetchall()
    first_last_day = (str_to_date(fetch_data[0][0]),
        str_to_date(fetch_data[0][1]))
    conn.close()
    return first_last_day
