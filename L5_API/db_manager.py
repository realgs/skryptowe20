import sqlite3
import L5_API.api_handler as api_hdl
from L5_API.constants import DB_FILE


def __connect_db():
    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)
    except sqlite3.Error as e:
        print('db_handler: connect_db ' + str(e))

    return conn


def __drop_rates_table():
    conn = __connect_db()
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE rates;""")

    conn.commit()
    conn.close()


def __create_rates_table():
    conn = __connect_db()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE rates (
                        RateDate data_type BLOB NOT NULL,
                        Rate data_type REAL NOT NULL,
                        Code data_type TEXT NOT NULL,
                        Interpolated BOOLEAN NOT NULL CHECK (Interpolated IN (0, 1)),
                        CONSTRAINT rates_pk PRIMARY KEY (RateDate, Code)
                   );""")

    conn.commit()
    conn.close()


def get_sales(date):
    conn = __connect_db()
    cursor = conn.cursor()

    sales = []

    try:
        cursor.execute("""SELECT Total FROM invoices
                            WHERE InvoiceDate = '{} 00:00:00'""".format(date))
        sales = [float(x[0]) for x in cursor.fetchall()]
    except sqlite3.Error as e:
        print('db_handler: get_sales ' + str(e))

    conn.close()

    return sales


def get_total_sale(date):
    return sum(get_sales(date))


def get_rate(date, currency_code):
    conn = __connect_db()
    cursor = conn.cursor()
    rate = 0.0

    try:
        cursor.execute("""SELECT Rate FROM rates
                            WHERE RateDate = '{}'
                            AND Code = '{}';""".format(date, currency_code))
        rate = float(cursor.fetchone()[0])
    except sqlite3.Error as e:
        print('db_handler: get_rate(' + date + ', ' + currency_code + ') ' + str(e))

    conn.close()

    return rate


def get_todays_date(currency_code):
    conn = __connect_db()
    cursor = conn.cursor()
    date = ''

    try:
        cursor.execute("""SELECT MAX(RateDate) FROM rates
                            WHERE Code = '{}';""".format(currency_code))
        date = cursor.fetchone()[0]
    except sqlite3.Error as e:
        print('db_handler: get_todays_date(' + currency_code + ') ' + str(e))

    conn.close()
    return date


def get_rates_dates_interpolated(currency_code, date_from, date_to):
    conn = __connect_db()
    cursor = conn.cursor()
    rates = []
    dates = []
    interpolated = []

    try:
        cursor.execute("""SELECT Rate, RateDate, Interpolated FROM rates
                            WHERE RateDate BETWEEN '{}' AND '{}'
                            AND Code = '{}';""".format(date_from, date_to, currency_code))
        for rate, date, ipd in cursor.fetchall():
            rates.append(float(rate))
            dates.append(date)
            interpolated.append(ipd)
    except sqlite3.Error as e:
        print('db_handler: get_rates' + str(e))

    conn.close()

    return rates, dates, interpolated


def get_sales_and_dates(date_from, date_to):
    conn = __connect_db()
    cursor = conn.cursor()

    sales = []
    dates = []

    try:
        cursor.execute("""SELECT SUM(Total), InvoiceDate FROM invoices
                                WHERE InvoiceDate BETWEEN '{}' AND '{}'
                                GROUP BY InvoiceDate""".format('{} 00:00:00'.format(date_from),
                                                               '{} 00:00:00'.format(date_to)))
        for sale, date in cursor.fetchall():
            sales.append(float(sale))
            dates.append(date[:10])
    except sqlite3.Error as e:
        print('db_handler: get_sales' + str(e))

    conn.close()

    return sales, dates


def add_rate_entry(date, rate, currency_code, interpolated):
    conn = __connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO rates VALUES (:RateDate, :Rate, :Code, :Interpolated)""",
                       {'RateDate': date, 'Rate': rate, 'Code': currency_code, 'Interpolated': interpolated})
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: add_rate_entry ' + str(e))

    conn.close()


def delete_rate_entry(date, currency_code):
    conn = __connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""DELETE FROM rates
                            WHERE RateDate = '{}'
                            AND Code = '{}'""".format(date, currency_code))
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: delete_rate_entry ' + str(e))

    conn.close()


def add_rate_entries(dates, rates, interpolated, currency_code):
    conn = __connect_db()
    cursor = conn.cursor()

    try:
        for i in range(len(dates)):
            cursor.execute("""INSERT INTO rates VALUES (:RateDate, :Rate, :Code, :Interpolated)""",
                           {'RateDate': dates[i],
                            'Rate': rates[i],
                            'Code': currency_code,
                            'Interpolated': interpolated[i]})
        conn.commit()
    except sqlite3.Error as e:
        print('db_handler: add_rate_entries ' + str(e))

    conn.close()


if __name__ == '__main__':
    date_from = '2009-01-01'
    date_to = '2020-12-17'

    # __drop_rates_table()
    # __create_rates_table()
    #
    # for currency in CURRENCIES:
    #     rates, dates, interpolated = api_hdl.currency_rates_dates_interpolated_time_frame(currency,
    #                                                                                       date_from,
    #                                                                                       date_to)
    #     add_rate_entries(dates, rates, interpolated, currency)
    # dates, rates, ipd = get_rates_dates_interpolated('USD', '2014-12-20', '2014-12-31')
    # print(dates)
    # print(rates)
    # print(ipd)
