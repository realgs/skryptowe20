import sqlite3
import json
from currency_rates import get_rete_of_currency
from datetime import datetime, timedelta


_DB_NAME = 'sales_database.db'
_DATE_FORMAT = '%Y-%m-%d'

def _create_USDRates_table():
    conn = sqlite3.connect(_DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE USDRates 
        (
            date DATE PRIMARY KEY NOT NULL,
            pln_cost FLOAT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def _append_missing_dates(rates):
    i = 0

    while i < len(rates) - 1:
        current = rates[i]
        next = rates[i + 1]

        curr_date = datetime.strptime(current['effectiveDate'], _DATE_FORMAT)
        next_date = datetime.strptime(next['effectiveDate'], _DATE_FORMAT)
        delta = next_date - curr_date

        if delta.days > 1:
            next_day = curr_date + timedelta(days=1)
            rates.insert(i + 1, {
                'effectiveDate': next_day.strftime(_DATE_FORMAT),
                'mid': current['mid']
            })

        i += 1

    return rates

def _update_dates():
    conn = sqlite3.connect(_DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE Orders
        SET OrderDate = DATETIME(OrderDate, '+10 years');
    ''')
    conn.commit()
    conn.close()
 

def _convert_to_tuples(rates):
    return [(e['effectiveDate'], e['mid']) for e in rates]

def _add_usd_rates():
    usd = get_rete_of_currency('usd', 365 * 25)
    rates = _append_missing_dates(usd['rates'])
    tuples = _convert_to_tuples(rates)

    conn = sqlite3.connect(_DB_NAME)
    c = conn.cursor()

    c.executemany('INSERT INTO USDRates VALUES (?, ?)', tuples)

    conn.commit()
    conn.close()

def get_transactions_usd_and_pln(begin, end):
    conn = sqlite3.connect(_DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT
            date,
            SUM(IFNULL(UnitPrice, 0) - IFNULL(Discount, 0) + IFNULL(Freight, 0)) AS USD,
            SUM((IFNULL(UnitPrice, 0) - IFNULL(Discount, 0) + IFNULL(Freight, 0)) * pln_cost) AS PLN
        FROM `Order Details`
        JOIN Orders USING(OrderID)
        JOIN USDRates
            ON strftime('%Y-%m-%d', OrderDate) = strftime('%Y-%m-%d', date)
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date;
    ''', (begin, end))
    res = c.fetchall()
    conn.close()
    return res

if __name__ == '__main__':
    _update_dates()
    _create_USDRates_table()
    _add_usd_rates()
