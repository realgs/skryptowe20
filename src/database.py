import sqlite3
import json
import nbp_api 
from datetime import datetime, timedelta


class NoSuchTableError(Exception):
    pass

__DB_NAME = 'sales.sqlite'

def __list_to_disc(lists):
    return [{"date":elem[0], "rate":elem[1], "interpolated": bool(elem[2]) } for elem in lists]

def __check_if_table_exists(conn, table_name):
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = ?''', (table_name,))
    if c.fetchone()[0] == 0:
        conn.close()
        raise NoSuchTableError('Such table does not exist')

def create_and_fill_currency_table(currency, delta):
    try:
        result = nbp_api.get_rete_of_currency(currency, delta)
        if result is not None:  
            tuples = [(rate['date'], rate['rate'], rate['interpolated']) for rate in result]
            conn = sqlite3.connect(__DB_NAME)
            c = conn.cursor()

            c.execute(f'''
                CREATE TABLE IF NOT EXISTS {currency.upper()} 
                (
                    date DATE PRIMARY KEY NOT NULL,
                    pln_cost REAL NOT NULL,
                    interpolated BOOLEAN NOT NULL CHECK (interpolated IN (0, 1))
                )
            ''')

            c.executemany(f'INSERT OR IGNORE INTO {currency.upper()} VALUES (?, ?, ?)', tuples)

            conn.commit()
            conn.close()

            return True
    except ValueError:
        pass
    return False

def get_between(currency, begin, end):
    if not isinstance(currency, str) or not isinstance(begin, str) or not isinstance(end, str):
        raise TypeError('Each parameter must be a string')

    datetime.strptime(begin, nbp_api.DATE_FORMAT)
    datetime.strptime(end, nbp_api.DATE_FORMAT)

    conn = sqlite3.connect(__DB_NAME)
    __check_if_table_exists(conn, currency)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {currency.upper()} WHERE date BETWEEN ? AND ? ORDER BY date', (begin, end))
    res = __list_to_disc(c.fetchall())
    conn.close()
    return res

def get_last(currency, delta):
    if not isinstance(delta, int):
        raise TypeError('Wrong parameter types') 

    if delta <= 0:
        raise ValueError('Delta must be positive')
    
    conn = sqlite3.connect(__DB_NAME)
    currency = currency.upper()
    __check_if_table_exists(conn, currency)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {currency} ORDER BY date DESC LIMIT ?', (delta,))
    res = __list_to_disc(c.fetchall())
    conn.close()
    return res


if __name__ == '__main__':
    # print(json.dumps(get_between('usd', '2020-01-01', '2020-10-10'), indent=4))
    print(json.dumps(get_last('eur', 10), indent=4))
