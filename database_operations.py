import sqlite3

DB_NAME = 'data.db'
DATE_FORMAT = "%Y-%m-%d"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as err:
        print(err)
    return conn

def create_rates_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS rates(rate_dates data PRIMARY KEY NOT NULL, rate real)''')
    conn.commit()
    conn.close()


def insert_rates(rate_vals):
    if len(rate_vals) < 1:
        print("Incorrect data")
        return
    conn = create_connection()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO rates VALUES (?, ?)", rate_vals)
    conn.commit()
    conn.close()


def get_transaction_sums_for_days(start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    interval=(start_date, end_date)
    sales_data = cursor.execute(
        f'''SELECT SUM(sales), orderdate, rate 
            FROM sales_table 
            JOIN rates ON orderdate = rate_dates
            WHERE rate_dates BETWEEN ? AND ?
            group by orderdate''', interval).fetchall()
    conn.close()

    return sales_data

def drop_rate_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE rates")
    conn.close()



