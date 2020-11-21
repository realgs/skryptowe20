import pyodbc

SALES_DATABASE = 'AdventureWorks2019.Sales.SalesOrderHeader'


def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-IN8O3LQ;'
                          'Database=AdventureWorks2019;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    return cursor


def add_col_to_db(cursor):
    cursor.execute('ALTER TABLE ' + SALES_DATABASE + ' ADD CurrencyRate float(1)')
    cursor.execute('ALTER TABLE ' + SALES_DATABASE + ' ADD CurrencyType varchar(3)')
    cursor.commit()


def fill_col_usd_rate(cursor, date_from_string, date_to_string, currency_date_list, currency_mid_list, currency_type):
    cursor.execute('SELECT * FROM ' + SALES_DATABASE + ' WHERE OrderDate BETWEEN \'' + date_from_string + '\' AND \'' +
                   date_to_string + '\'')
    select_list = []
    for row in cursor:
        select_list.append(row)
    currency_index = 0
    for row in select_list:
        row_date = row[2]
        while row_date != currency_date_list[currency_index]:
            if row_date < currency_date_list[currency_index]:
                currency_index = 0
            currency_index += 1
        cursor.execute('UPDATE ' + SALES_DATABASE + ' SET CurrencyRate = ' + str(currency_mid_list[currency_index]) +
                       ', CurrencyType = \'' + str(currency_type) + '\' WHERE SalesOrderID = ' + str(row[0]))
        cursor.commit()


def get_total_sales_to_chart(cursor, date_from_string, date_to_string):
    cursor.execute('SELECT OrderDate, SUM(TotalDue), MAX(CurrencyRate) FROM ' + SALES_DATABASE + ' WHERE OrderDate BETWEEN \'' + date_from_string + '\' AND \'' +
                   date_to_string + '\' GROUP BY OrderDate ORDER BY OrderDate')
    total_sales_list = []
    for row in cursor:
        total_sales_list.append(row)
    return total_sales_list