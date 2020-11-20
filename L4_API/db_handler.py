import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib import dates

DB_FILE = 'sales.db'
PLOT_TICKS = 30
WIDTH = 0.1
PLOT_SIZE_X = 10
PLOT_SIZE_Y = 5


def connect_db():
    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)
    except sqlite3.Error as e:
        print('db_handler: connect_db ' + e)

    return conn


def get_sales(date):
    conn = connect_db()
    cursor = conn.cursor()

    sales = []
    date += ' 00:00:00'

    try:
        cursor.execute("""SELECT Total FROM invoices
                            WHERE InvoiceDate = '{}'""".format(date))
        sales = [float(x[0]) for x in cursor.fetchall()]
    except sqlite3.Error as e:
        print('db_handler: get_sales ' + e)

    conn.close()

    return sales


def get_total_sale(date):
    return sum(get_sales(date))


def get_rate(date, currency_code):
    conn = connect_db()
    cursor = conn.cursor()
    rate = ''

    cursor.execute("""SELECT Rate FROM rates
                    WHERE RateDate = '{}'
                    AND Code = '{}';""".format(date, currency_code))
    try:
        rate = str(cursor.fetchone()[0])
    except TypeError as e:
        print('db_handler: get_rate(' + date + ', ' + currency_code + ') ' + str(e))

    conn.close()

    return rate


def create_rates_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE rates (
                        RateDate data_type BLOB,
                        Rate data_type REAL,
                        Code data_type TEXT
                   );""")

    conn.commit()
    conn.close()


def add_rate_entry(date, rate, currency_code):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO rates VALUES (:RateDate, :Rate, :Code)""",
                   {'RateDate': date, 'Rate': rate, 'Code': currency_code})

    conn.commit()
    conn.close()


def plot_data(currency_code, date_from, date_to):
    dates = []
    sales = []
    rates = []
    sales_pln = []

    date = date_from
    while date <= date_to:
        sale = get_total_sale(date)
        rate = float(get_rate(date, currency_code))
        dates.append(date)
        sales.append(sale)
        rates.append(rate)
        sales_pln.append(sale * rate)

        new_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        date = new_date.strftime('%Y-%m-%d')

    return dates, sales, rates, sales_pln


def plot(currency_code, date_from, date_to):
    sale_dates, sales, rates, sales_pln = plot_data(currency_code, date_from, date_to)
    x_min = date_from
    x_max = date_to

    plt.figure(figsize=(PLOT_SIZE_X, PLOT_SIZE_Y))
    plt.subplots_adjust(left=0.1, bottom=0.2)

    plt.plot(sale_dates, sales_pln, linewidth=0.8, label='PLN')
    plt.plot(sale_dates, sales, linewidth=0.8, label='USD')

    plt.title("Sprzedaż w dniach od {} do {}".format(x_min, x_max))
    plt.xlabel("data")
    plt.ylabel("sprzedaż")

    plt.legend(frameon=False, loc='best')
    plt.grid(axis='y', lw=0.25)
    plt.xlim(x_min, x_max)
    _, ticks = plt.xticks()
    for i, tick in enumerate(ticks):
        tick.set_fontsize(8)
        tick.set_rotation(45)
        if i % PLOT_TICKS != 0:
            tick.set_visible(False)

    plt.show()


if __name__ == '__main__':
    # create_rates_table()
    pass
