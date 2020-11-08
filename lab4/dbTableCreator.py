from datetime import date

import psycopg2
from psycopg2 import OperationalError
import json
import time

from app.src.nbpRatesReceiver import get_currency_rates

CONFIG_PATH = 'app/src/dbConfig.json'
USD_RATES_TABLE = 'usd_rates'
USD_CODE = 'usd'


def create_connector(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Exception as exc:
        print(f"The error '{exc}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")


def insert_data(connector, table_name, table_row_structure, data, log_inserted_data=False):
    records = ", ".join(["%s"] * len(data))
    insertion_start = time.time()
    insert_query = (f"INSERT INTO {table_name} {table_row_structure} OVERRIDING SYSTEM VALUE VALUES {records}")
    connector.autocommit = True
    cursor = connector.cursor()
    cursor.execute(insert_query, data)
    insertion_time = time.time() - insertion_start
    read_start = time.time()
    select_inserted_data = f"SELECT * FROM {table_name}"
    inserted_data = execute_read_query(connector, select_inserted_data)
    read_time = time.time() - read_start
    if log_inserted_data:
        print(f"Operation on table: '{table_name}' completed. Inserted rows:")
        for i, row in enumerate(inserted_data):
            print(f'      {i + 1}.)    {row}')
        print(f"  - Number of inserted rows: {len(inserted_data)}")
        print(f"  - Insertion time: {round(insertion_time, 4)} seconds")
        print(f"  - Read time: {round(read_time, 4)} seconds")
        print()
    return inserted_data


def read_from_file(file_name):
    with open(file_name) as file:
        return file.read()


if __name__ == '__main__':
    conf = json.loads(read_from_file(CONFIG_PATH))
    db_connector = create_connector(conf["dbname"], conf["user"], conf["password"], conf["host"], conf["port"])
    execute_query(db_connector, read_from_file(conf['script']))

    result1, status1 = get_currency_rates(USD_CODE, date(2019, 1, 1), date(2019, 12, 31))
    result2, status2 = get_currency_rates(USD_CODE, date(2020, 1, 1), date(2020, 11, 1))

    rates = result1['rates'] + result2['rates']

    usd_rates_data = []
    print(rates)
    for i, exchange_rate in enumerate(rates):
        usd_rate = (i + 1, exchange_rate['date'], exchange_rate['rate'])
        usd_rates_data.append(usd_rate)

    insert_data(db_connector, USD_RATES_TABLE, '(usd_rate_id, date, rate)', usd_rates_data, True)
