from datetime import datetime, timedelta
import sqlite3
import json

DB_NAME = "../../Source/bazunia.db"


class Database:
    DATEFORMAT = "%Y-%m-%d"
    currencies = ['pln', 'eur', 'chf', 'usd']

    def __init__(self, db_source):
        self.db_source = db_source


    def get_min_max_dates(self):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()
        c.execute("""
            SELECT MIN(OrderDate), MAX(OrderDate) FROM Orders
        """)
        res = c.fetchall()
        conn.close()

        return res


    def create_avg_currency_rates_table(self):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()
        c.execute(
        '''
        CREATE TABLE if not exists AvgRates (
            avg_usd REAL NOT NULL,
            avg_eur REAL NOT NULL,
            avg_chf REAL NOT NULL,
            date DATE PRIMARY KEY NOT NULL,
            interpolated BOOLEAN NOT NULL DEFAULT FALSE
        )
        '''
        )
        conn.commit()
        conn.close()


    def get_sales_usd_another_currency(self, start_date, end_date, currency='pln'):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()
        if currency not in self.currencies:
            return []
        if currency == 'pln':
            currency = '1'
        else:
            currency = ' `rates`.avg_' + currency
        print(currency)
        c.execute(
            f'''
            SELECT
            date,
                SUM(IFNULL(UnitPrice, 0) - IFNULL(Discount, 0) + IFNULL(Freight, 0)) AS original,
                SUM((IFNULL(UnitPrice, 0) - IFNULL(Discount, 0) + IFNULL(Freight, 0)) / {currency} * `rates`.avg_usd ) AS requested
            FROM `Order Details`
            JOIN Orders USING(OrderID)
            JOIN AvgRates AS rates ON strftime('%Y-%m-%d', OrderDate) = strftime('%Y-%m-%d', date)
            WHERE strftime('%Y-%m-%d', date) BETWEEN ? AND ?
            GROUP BY date
            ORDER BY date
            ''', (start_date, end_date)
        )
        res = c.fetchall()
        conn.close()

        return res


    def get_avg_rates(self, date=None):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()
        res = None

        if date is None:
            c.execute("""SELECT * FROM AvGRates ORDER BY date""")
            res = c.fetchall()
        else:
            c.execute("""SELECT * FROM AvGRates WHERE strftime(?, date) = strftime(?, ?) """, (self.DATEFORMAT, self.DATEFORMAT, date))
            res = c.fetchall()

        conn.commit()
        conn.close()

        return res


    def get_avg_rates_in_interval(self, start_date=None, end_date=None):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()

        c.execute("""SELECT * FROM AvGRates WHERE strftime('%Y-%m-%d', date) BETWEEN ? AND ? ORDER BY date""", (start_date, end_date))
        res = c.fetchall()

        conn.commit()
        conn.close()

        return res


    def _add_missing_dates(self, rates):
        for i in range(len(rates) - 1):
            curr = rates[i]
            next = rates[i + 1]

            curr_date = datetime.strptime(curr[3], self.DATEFORMAT)
            next_date = datetime.strptime(next[3], self.DATEFORMAT)
            delta = next_date - curr_date

            if delta.days > 1:
                next_day = curr_date + timedelta(days=1)
                if next_day.strftime(self.DATEFORMAT) not in [x[3] for x in rates]:
                    rates.insert(i + 1, (
                        curr[0],
                        curr[1],
                        curr[2],
                        next_day.strftime(self.DATEFORMAT),
                        True
                    ))
        return rates


    def insert_rates(self, start_date, end_date):
        from nbp import fetch_currency_from_two_tables

        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()

        rates_usd = fetch_currency_from_two_tables(start_date, end_date, currency='usd')
        rates_eur = fetch_currency_from_two_tables(start_date, end_date, currency='eur')
        rates_chf = fetch_currency_from_two_tables(start_date, end_date, currency='chf')

        rates = [(rates_usd[x][0], rates_eur[x][0], rates_chf[x][0], rates_eur[x][1], False) for x in range(len(rates_usd))]

        new_rates = self._add_missing_dates(rates)

        c.execute('SELECT date FROM AvgRates')
        db_rates = c.fetchall()
        to_insert = []

        for x in new_rates:
            if x[1] not in db_rates:
                to_insert.append(x)

        c.executemany('INSERT INTO AvgRates VALUES (?, ?, ?, ?, ?)', to_insert)
        conn.commit()


if __name__ == "__main__":
    db_source = "../../Source/bazunia.db"

    db = Database(db_source)

    [(min_date, max_date)] = db.get_min_max_dates()

    print(db.get_avg_rates_in_interval(min_date, max_date))
