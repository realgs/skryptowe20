import sqlite3
import json
import nbp_api 
from datetime import datetime, timedelta
from keys import *


class NoSuchTableError(Exception):
    pass

__DB_NAME = 'sales.sqlite'

def __rates_list_to_disc(lists):
    return [{DATE_KEY:elem[0], RATE_KEY:elem[1], INTERPOLATED_KEY: bool(elem[2]) } for elem in lists]

def __sales_list_to_disc(lists, currency):
    return [{DATE_KEY:elem[0], 'USD':elem[1], currency: elem[2]} for elem in lists]

def __rates_dict_to_tuple(dictionaries):
    return [(elem[DATE_KEY], elem[RATE_KEY], elem[INTERPOLATED_KEY]) for elem in dictionaries]

def __check_if_table_exists(conn, table_name):
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = ?''', (table_name,))
    if c.fetchone()[0] == 0:
        conn.close()
        raise NoSuchTableError('Such table does not exist')

def create_and_fill_rates_table(currency, delta):
    try:
        result = nbp_api.get_rete_of_currency(currency, delta)
        if result is not None:  
            result = __rates_dict_to_tuple(result)
            conn = sqlite3.connect(__DB_NAME)
            c = conn.cursor()

            c.execute(f'''
                CREATE TABLE IF NOT EXISTS {currency.upper()} 
                (
                    date DATE PRIMARY KEY NOT NULL,
                    rate REAL NOT NULL,
                    interpolated BOOLEAN NOT NULL CHECK (interpolated IN (0, 1))
                )
            ''')

            c.executemany(f'INSERT OR IGNORE INTO `{currency.upper()}` VALUES (?, ?, ?)', result)

            conn.commit()
            conn.close()

            return True
    except ValueError:
        pass
    return False

def get_rates_between(currency, begin, end):
    if not isinstance(currency, str) or not isinstance(begin, str) or not isinstance(end, str):
        raise TypeError('Each parameter must be a string')

    datetime.strptime(begin, DATE_FORMAT)
    datetime.strptime(end, DATE_FORMAT)

    conn = sqlite3.connect(__DB_NAME)
    __check_if_table_exists(conn, currency)
    c = conn.cursor()
    c.execute(f'SELECT * FROM `{currency.upper()}` WHERE date BETWEEN ? AND ? ORDER BY date', (begin, end))
    res = __rates_list_to_disc(c.fetchall())
    conn.close()
    return res

def get_rates_last(currency, delta):
    if not isinstance(delta, int):
        raise TypeError('Wrong parameter types') 

    if delta <= 0:
        raise ValueError('Delta must be positive')
    
    conn = sqlite3.connect(__DB_NAME)
    currency = currency.upper()
    __check_if_table_exists(conn, currency)
    c = conn.cursor()
    c.execute(f'SELECT * FROM `{currency}` ORDER BY date DESC LIMIT ?', (delta,))
    res = __rates_list_to_disc(c.fetchall())
    conn.close()
    return res

def get_sales_between(desired_currency, begin, end):
    if not isinstance(desired_currency, str) or not isinstance(begin, str) or not isinstance(end, str):
        raise TypeError('Each parameter must be a string')

    datetime.strptime(begin, DATE_FORMAT)
    datetime.strptime(end, DATE_FORMAT)

    desired_currency = desired_currency.upper()

    conn = sqlite3.connect(__DB_NAME)
    __check_if_table_exists(conn, desired_currency)
    c = conn.cursor()
    c.execute(f'''
        SELECT
            `OrderDate`,
            ROUND(SUM(`UnitPrice` * `Quantity` * ( 1 - `Discount`)), 2),
            ROUND(SUM(`UnitPrice` * `Quantity` * ( 1 - `Discount`) / `{desired_currency}`.rate * `USD`.rate), 2)
        FROM `Order`
        JOIN `OrderDetail`
            ON `Order`.`Id` = `OrderDetail`.`OrderId`
        JOIN `{desired_currency}`
            ON `{desired_currency}`.date = `Order`.`OrderDate`
        JOIN `USD`
            ON `USD`.date = `Order`.`OrderDate`
        WHERE `OrderDate` BETWEEN ? AND ?
        GROUP BY `OrderDate`''', (begin, end))
    res = __sales_list_to_disc(c.fetchall(), desired_currency)
    conn.close()
    return res

if __name__ == '__main__':
    # print(json.dumps(get_between('usd', '2020-01-01', '2020-10-10'), indent=4))
    print(json.dumps(get_last('eur', 10), indent=4))
