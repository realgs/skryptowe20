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

    cursor.execute("""SELECT Total
                    FROM invoices
                    WHERE InvoiceDate = {}""".format(date))
    sales = cursor.fetchall()
    conn.close()

    return sales
