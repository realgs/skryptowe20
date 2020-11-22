import pyodbc

SALES_TABLE = 'Sales.SalesOrderHeader'
MY_TABLE = 'Currency'


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


def get_data_from_database(cursor, date_from, date_to):
    sales_list = []
    rates_list = []
    merged_list = []

    cursor.execute(f"""
    SELECT OrderDate, SUM(TotalDue)
    FROM {SALES_TABLE}
    WHERE OrderDate BETWEEN \'{date_from}\' AND \'{date_to}\'
    GROUP BY OrderDate
    ORDER BY OrderDate
    """)

    for row in cursor:
        sales_list.append(row)

    cursor.execute(f"""
    SELECT CurrencyRate
    FROM {MY_TABLE}
    """)

    for row in cursor:
        rates_list.append(row)

    for i in range(len(sales_list)):
        merged_list.append((sales_list[i][0], sales_list[i][1], rates_list[i][0]))

    return merged_list
