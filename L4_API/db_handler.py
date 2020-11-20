import sqlite3

DB_FILE = 'sales.db'


def connect_db():
    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)
    except sqlite3.Error as e:
        print(e)

    return conn


def get_sales(date):
    conn = connect_db()
    cursor = conn.cursor()
    date += ' 00:00:00'

    cursor.execute("""SELECT Total
                    FROM invoices
                    WHERE InvoiceDate = '{}'""".format(date))
    sales = [x[0] for x in cursor.fetchall()]
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
        print(e)

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


if __name__ == '__main__':
    # create_rates_table()
    # add_rate_entry('2020-01-01', 8.1203, 'JOD')

    conn = connect_db()
    cursor = conn.cursor()

    # cursor.execute("""DELETE FROM rates WHERE Code = 'JOD'""")
    # conn.commit()

    cursor.execute("""SELECT * FROM rates""")
    print(cursor.fetchall())
    conn.close()

    # print(get_rate('2020-01-01', 'JOD'))
