import pyodbc

SALES_TABLE = 'Sales.SalesOrderHeader'
MY_TABLE = 'Currency'


def test(cursor):
    cursor.execute(f'SELECT * FROM {MY_TABLE};')
    for row in cursor:
        print(row)


def connect():
    conn = pyodbc.connect('Driver={SQL Server};Server=DESKTOP-1A5C2CG;'
                          'Database=AdventureWorks2019;Trusted_Connection=yes;')
    cursor = conn.cursor()
    return conn, cursor


def create_table(cursor):
    cursor.execute('''
    CREATE TABLE Currency (
        QuotationDate DATETIME PRIMARY KEY,
        CurrencyRate REAL NOT NULL
        );
    ''')


def fill_table(conn, cursor, date_list, rate_list):
    for i in range(len(date_list)):
        cursor.execute('''
        INSERT INTO Currency (QuotationDate, CurrencyRate)
        VALUES (?,?)''',
                       date_list[i], rate_list[i])
    conn.commit()
