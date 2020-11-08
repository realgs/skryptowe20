import json
import time

import psycopg2

USD_RATES_TABLE = 'usd_rates'
ORDERS_TABLE = 'orders'
SELECT_USD_RATES_SQL_QUERY = f"SELECT date, rate FROM {USD_RATES_TABLE} SORT ORDER BY date"
SELECT_ORDERS_SQL_QUERY = f"SELECT orderid, orderdate, totalamount FROM {ORDERS_TABLE} ORDER BY orderdate "


def execute_read_query(connection, query):
    read_start = time.time()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        read_time = time.time() - read_start
        print(f"Read operation on table: '{USD_RATES_TABLE}' completed. Number of rows: {len(result)}. "
              f"Operation time: {round(read_time, 4)} seconds.")
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")


def read_from_file(file_name):
    with open(file_name) as file:
        return file.read()


class DataAccessObject:

    def __init__(self, db_config_file_path):
        conf = json.loads(read_from_file(db_config_file_path))
        self.db_connector = psycopg2.connect(
            database=conf["dbname"], user=conf["user"], password=conf["password"], host=conf["host"], port=conf["port"],
        )
        print("Connection to PostgreSQL DB was successfully established")

    def read_usd_pln_rates(self):
        raw_usd_rate_rows = execute_read_query(self.db_connector, SELECT_USD_RATES_SQL_QUERY)
        return list(map(lambda row: {"date": row[0], "plnRate": row[1]}, raw_usd_rate_rows))

    def read_orders(self):
        raw_order_rows = execute_read_query(self.db_connector, SELECT_ORDERS_SQL_QUERY)
        return list(map(lambda row: {"id": row[0], "date": row[1], "totalAmount": row[2]}, raw_order_rows))
