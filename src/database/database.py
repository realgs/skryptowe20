from datetime import datetime, timedelta
import sqlite3
import json

DB_NAME = "../../Source/bazunia.db"


class Database:
    DATEFORMAT = "%Y-%m-%d"


    def __init__(self, db_source):
        self.db_source = db_source


    def create_avg_currency_rates_table(self):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()
        c.execute(
        '''
        CREATE TABLE if not exists AvgUsdRates (
            avg_rates REAL NOT NULL,
            date DATE PRIMARY KEY NOT NULL,
            interpolated BOOLEAN NOT NULL DEFAULT FALSE
        )
        '''
        )
        conn.commit()
        conn.close()


    def _add_missing_dates(self, rates):
        for i in range(len(rates) - 1):
            curr = rates[i]
            next = rates[i + 1]

            curr_date = datetime.strptime(curr[1], self.DATEFORMAT)
            next_date = datetime.strptime(next[1], self.DATEFORMAT)
            delta = next_date - curr_date

            if delta.days > 1:
                next_day = curr_date + timedelta(days=1)
                if next_day.strftime(self.DATEFORMAT) not in [x[1] for x in rates]:
                    rates.insert(i + 1, (
                        curr[0],
                        next_day.strftime(self.DATEFORMAT),
                        True
                    ))
        return rates


    def get_sales_usd_pln(self, start_date, end_date):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()

        c.execute(
            '''
            SELECT
            date,
                SUM(IFNULL(UnitPrice, 0) - IFNULL(Discount, 0) + IFNULL(Freight, 0)) AS usd,
                SUM((IFNULL(UnitPrice, 0) - IFNULL(Discount, 0) + IFNULL(Freight, 0)) * avg_rates) AS pln
            FROM `Order Details`
            JOIN Orders USING(OrderID)
            JOIN AvgUsdRates ON strftime('%Y-%m-%d', OrderDate) = strftime('%Y-%m-%d', date)
            WHERE strftime('%Y-%m-%d', date) BETWEEN ? AND ?
            GROUP BY date
            ORDER BY date
            ''', (start_date, end_date)
        )
        res = c.fetchall()
        conn.close()

        return res


    def get_avg_usd_rates(self, date=None):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()
        res = None

        if date is None:
            c.execute("""SELECT * FROM AvGUsdRates ORDER BY date""")
            res = c.fetchall()
        else:
            c.execute("""SELECT * FROM AvGUsdRates WHERE strftime(?, date) = strftime(?, ?) """, (self.DATEFORMAT, self.DATEFORMAT, date))
            res = c.fetchall()

        conn.commit()
        conn.close()

        return res


    def get_avg_usd_rates_in_interval(self, start_date=None, end_date=None):
        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()

        c.execute("""SELECT * FROM AvGUsdRates WHERE strftime('%Y-%m-%d', date) BETWEEN ? AND ? ORDER BY date""", (start_date, end_date))
        res = c.fetchall()

        conn.commit()
        conn.close()

        return res


    def insert_usd_rates(self, start_date, end_date):
        from nbp import fetch_currency_from_two_tables

        conn = sqlite3.connect(self.db_source)
        c = conn.cursor()

        rates = fetch_currency_from_two_tables(start_date, end_date)
        # new_rates = rates
        new_rates = self._add_missing_dates(rates)

        c.execute('SELECT date FROM AvgUsdRates')
        db_rates = c.fetchall()
        to_insert = []

        for x in new_rates:
            if x[1] not in db_rates:
                to_insert.append(x)

        c.executemany('INSERT INTO AvgUsdRates VALUES (?, ?, ?)', to_insert)
        conn.commit()
