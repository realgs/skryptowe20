import json
import time
import psycopg2
import logging


def execute_read_query(connection, query, table_name):
    read_start = time.time()
    cursor = connection.cursor()
    logging.info(f'Executing query: {query} ...')
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        read_time = time.time() - read_start
        logging.info(f'Read operation on table: {table_name} completed. Number of rows: {len(result)}. '
                     f'Operation time: {round(read_time, 4)} seconds.')
        return result
    except Exception as e:
        logging.error(f'The error: {e} occurred')
        raise e


def read_from_file(file_name):
    with open(file_name) as file:
        return file.read()


class DataAccessObject:

    def __init__(self, db_config_file_path):
        conf = json.loads(read_from_file(db_config_file_path))
        while True:
            conn = psycopg2.connect(
                database=conf['dbname'],
                user=conf['user'],
                password=conf['password'],
                host=conf['host'],
                port=conf['port'],
            )
            cur = conn.cursor()
            try:
                cur.execute('select 1;')
            except psycopg2.OperationalError:
                continue
            self.db_connector = conn
            break
        logging.info('Connection to PostgreSQL DB was successfully established')

    def read_orders(self, start_date, end_date):
        query = f"SELECT orderid, orderdate, totalamount " \
                f"FROM orders " \
                f"WHERE orderdate BETWEEN '{start_date}' and '{end_date}' " \
                f"ORDER BY orderdate"
        raw_order_rows = execute_read_query(self.db_connector, query, 'orders')
        return list(map(lambda row: {'id': row[0], 'date': row[1], 'totalAmount': row[2]}, raw_order_rows))
