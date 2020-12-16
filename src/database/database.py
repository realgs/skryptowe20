from datetime import datetime, timedelta
import sqlite3
import json
# from nbp import fetch_currency_from_two_tables, from_json_to_list


DB_NAME = "../../Source/bazunia.db"
TIME_DELTA = 182

class Database:
    DATEFORMAT = "%Y-%m-%d"


    def __init__(self, db_source):
        self.conn = sqlite3.connect(db_source)


    def create_avg_currency_rates_table(self):
        c = self.conn.cursor()
        c.execute(
        '''
        CREATE TABLE if not exists AvgUsdRates (
            avg_rates REAL NOT NULL,
            date DATE PRIMARY KEY NOT NULL,
            interpolated BOOLEAN NOT NULL DEFAULT FALSE
        )
        '''
        )
        self.conn.commit()


    # def insert_usd_rates(self, start_date, end_date):
    #     c = self.conn.cursor()

    #     rates = fetch_currency_from_two_tables(start_date, end_date)
    #     new_rates = set(self._add_missing_dates(rates))

    #     c.execute('SELECT * FROM AvgUsdRates')
    #     db_rates = c.fetchall()
    #     to_insert = new_rates - set(db_rates)
    #     print(to_insert)

    #     c.executemany('INSERT INTO AvgUsdRates VALUES (?, ?, ?)', to_insert)
    #     self.conn.commit()


    def _add_missing_dates(self, rates):
        for i in range(len(rates) - 1):
            curr = rates[i]
            next = rates[i + 1]

            curr_date = datetime.strptime(curr[1], self.DATEFORMAT)
            next_date = datetime.strptime(next[1], self.DATEFORMAT)
            delta = next_date - curr_date

            if delta.days > 1:
                next_day = curr_date + timedelta(days=1)
                rates.insert(i + 1, (
                    curr[0],
                    next_day.strftime(self.DATEFORMAT),
                    True
                ))
        return rates


    def update_dates(self, conn, years):
        c = self.conn.cursor()

        c.execute(
            f'''
            UPDATE Orders
            SET OrderDate = DATETIME(OrderDate, '+{years} YEARS')
            WHERE DATETIME(OrderDate, '+{years} YEARS') < date('now')
            '''
        )


    def get_sales_usd_pln(self, start_date, end_date):
        c = self.conn.cursor()

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
            ''', (start_date, end_date)
        )
        res = c.fetchall()
        return res


    def get_avg_usd_rates(self, date=None):
        c = self.conn.cursor()

        if date is None:
            c.execute("""SELECT * FROM AvGUsdRates ORDER BY date""")
            return c.fetchall()
        else:
            c.execute("""SELECT * FROM AvGUsdRates WHERE strftime(?, date) = strftime(?, ?) """, (self.DATEFORMAT, self.DATEFORMAT, date))
            return c.fetchall()


    def closeConn(self):
        self.conn.close()


if __name__ == "__main__":
    start_date = '2011-07-04'
    end_date = '2013-05-06'

    db = Database(DB_NAME)
    print(db.get_avg_usd_rates(start_date))
    print(db.get_avg_usd_rates('2020-12-12'))
    # DB OPERATIONS
    # create_avg_currency_rates_table(conn)
    # insert_usd_rates(conn, start_date, end_date)
    # update_dates(conn, 15)
