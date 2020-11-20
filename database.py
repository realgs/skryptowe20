from datetime import datetime, timedelta
import sqlite3
import json
import matplotlib
import matplotlib.pyplot as plt
from nbp import fetch_currency_from_two_tables, from_json_to_list


DB_NAME = "Source/bazunia.db"
DATEFORMAT = "%Y-%m-%d"
TIME_DELTA = 182


def create_avg_currency_rates_table(conn):
    c = conn.cursor()
    c.execute(
    '''
    CREATE TABLE if not exists AvgUsdRates (
        avg_rates REAL NOT NULL,
        date DATE PRIMARY KEY NOT NULL
    )
    '''
    )
    conn.commit()


def insert_usd_rates(conn, start_date, end_date):
    rates = fetch_currency_from_two_tables(start_date, end_date)
    new_rates = set(add_missing_dates(rates))

    c = conn.cursor()
    c.execute('SELECT * FROM AvgUsdRates')
    db_rates = c.fetchall()
    to_insert = new_rates - set(db_rates)
    print(to_insert)

    c.executemany('INSERT INTO AvgUsdRates VALUES (?, ?)', to_insert)
    conn.commit()


def add_missing_dates(rates):
    for i in range(len(rates) - 1):
        curr = rates[i]
        next = rates[i + 1]

        curr_date = datetime.strptime(curr[1], DATEFORMAT)
        next_date = datetime.strptime(next[1], DATEFORMAT)
        delta = next_date - curr_date

        if delta.days > 1:
            next_day = curr_date + timedelta(days=1)
            rates.insert(i + 1, (
                curr[0],
                next_day.strftime(DATEFORMAT)
            ))
    return rates


def update_dates(conn, years):
    c = conn.cursor()
    c.execute(
        f'''
        UPDATE Orders
        SET OrderDate = DATETIME(OrderDate, '+{years} YEARS')
        WHERE DATETIME(OrderDate, '+{years} YEARS') < date('now')
        '''
    )


def get_sales_usd_pln(conn, start_date, end_date):
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
        ''', (start_date, end_date)
    )
    res = c.fetchall()
    return res


def plot_database(x, y1, y2, label1=' ', label2=' ', xlabel=' ', ylabel=' ', title=' '):
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.15)
    ax.plot(x, y1, label=label1)
    ax.plot(x, y2, label=label2)
    ax.set(xlabel=xlabel, ylabel=ylabel,
            title=title)
    ax.set_xticks(ax.get_xticks()[::len(ax.get_xticks()) // 4])
    ax.legend()
    plt.xticks(rotation=20)
    fig.savefig(f'plots/{title}.svg')
    plt.show()


if __name__ == "__main__":
    start_date = '2011-07-04'
    end_date = '2013-05-06'

    conn = sqlite3.connect(DB_NAME)
    conn.text_factory = bytes

    # DB OPERATIONS
    create_avg_currency_rates_table(conn)
    # insert_usd_rates(conn, start_date, end_date)
    update_dates(conn, 15)
    sales = get_sales_usd_pln(conn, start_date, end_date)
    print(sales)

    conn.close()

    dates, usd, pln = zip(*sales)
    plot_database(
        dates,
        usd,
        pln,
        'USD',
        'PLN',
        xlabel='days',
        ylabel='avg currency',
        title=f'Sales values (EUR, USD) from {start_date} to {end_date}')
