import sqlite3
import json
from interpollator import nbp_api_interpolator
from datetime import datetime, timedelta
from nbp_api import nbp_api


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class database:

    DB_NAME = 'sales.sqlite'
    DATE_FORMAT = nbp_api.DATE_FORMAT

    def __init__(self):
        self.interpolator = nbp_api_interpolator()

    def create_currency_table(self, currency, delta):
        result = self.interpolator.get_currency(currency, delta)
        if result != []:  
            table_name = currency.upper()
            conn = sqlite3.connect(self.DB_NAME)
            c = conn.cursor()
            c.execute(f'DROP TABLE IF EXISTS `{table_name}`')
            c.execute(f'''
                CREATE TABLE {table_name} 
                (
                    date DATE PRIMARY KEY NOT NULL,
                    exchange_rate REAL NOT NULL,
                    interpolated BOOLEAN NOT NULL CHECK (interpolated IN (0, 1))
                )
            ''')
            c.executemany(f'INSERT INTO `{table_name}`(date, exchange_rate, interpolated) VALUES (:date, :exchange_rate, :interpolated)', [elem.toJSON() for elem in result])
            conn.commit()
            conn.close()

    def get_currency_between(self, currency, begin, end):
        conn = sqlite3.connect(self.DB_NAME)
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(f'SELECT * FROM `{currency.upper()}` WHERE date BETWEEN ? AND ? ORDER BY date', (begin.strftime(self.DATE_FORMAT), end.strftime(self.DATE_FORMAT)))
        res = c.fetchall()
        conn.close()
        return res

    def get_currency(self, currency, delta):
        conn = sqlite3.connect(self.DB_NAME)
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(f'SELECT * FROM `{currency.upper()}` ORDER BY date DESC LIMIT ?', (delta,))
        res = c.fetchall()
        conn.close()
        return res

    def get_sales_between(self, currency, begin, end):
        conn = sqlite3.connect(self.DB_NAME)
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(f'''
            SELECT
                `OrderDate` AS date,
                ROUND(SUM(`UnitPrice` * `Quantity` * ( 1 - `Discount`)), 2) AS original,
                ROUND(SUM(`UnitPrice` * `Quantity` * ( 1 - `Discount`) / `DESIRED`.`exchange_rate` * `USD`.`exchange_rate`), 2) AS requested
            FROM `Order`
            JOIN `OrderDetail`
                ON `Order`.`Id` = `OrderDetail`.`OrderId`
            JOIN `{currency.upper()}` AS DESIRED
                ON `DESIRED`.date = `Order`.`OrderDate`
            JOIN `USD`
                ON `USD`.date = `Order`.`OrderDate`
            WHERE `OrderDate` BETWEEN ? AND ?
            GROUP BY `OrderDate`''', (begin.strftime(self.DATE_FORMAT), end.strftime(self.DATE_FORMAT)))
        res = c.fetchall()
        conn.close()
        return res


if __name__ == '__main__':
    db = database()
    for elem in db.get_currency_between('eur', datetime(2020, 10, 10), datetime(2020, 12, 12)):
        print(elem)
    for elem in db.get_currency('eur', 30):
        print(elem)
    for elem in db.get_sales_between('eur', datetime(2010, 10, 10), datetime(2020, 12, 12)):
        print(elem)

