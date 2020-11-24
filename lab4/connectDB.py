import pyodbc

SALES_DATABASE = 'AdventureWorks2019'
NAME_SALES_TABLE = 'Sales.SalesOrderHeader'
NAME_CURRENCY_TABLE = 'Sales.UsdRate'


def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-IN8O3LQ;'
                          'Database=AdventureWorks2019;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    return cursor


def add_table_to_db(cursor):
    cursor.execute(f"CREATE TABLE {NAME_CURRENCY_TABLE} (RateDate DATETIME PRIMARY KEY, CurrencyRate REAL NOT NULL)")
    cursor.commit()


def fill_table_usd_rate(cursor, currency_date_list, currency_mid_list):
    currency_table = download_currency_table(cursor)
    for i in range(len(currency_date_list)):
        if not find_date_in_table(currency_table, currency_date_list[i]):
            cursor.execute(f"INSERT INTO {SALES_DATABASE}.{NAME_CURRENCY_TABLE} (RateDate, CurrencyRate) VALUES ("
                           f"\'{currency_date_list[i]}\',{currency_mid_list[i]})")
            cursor.commit()


def find_date_in_table(data, date_to_find):
    return date_to_find in data


def download_currency_table(cursor):
    cursor.execute(f"SELECT RateDate FROM {SALES_DATABASE}.{NAME_CURRENCY_TABLE} ORDER BY RateDate")
    select_list = []
    for row in cursor:
        select_list.append(row[0])
    return select_list


def get_total_sales_to_chart(cursor, date_from_string, date_to_string):
    cursor.execute(f"SELECT OrderDate, SUM(TotalDue) FROM {SALES_DATABASE}.{NAME_SALES_TABLE} WHERE OrderDate BETWEEN "
                   f"\'{date_from_string}\' AND \'{date_to_string}\' GROUP BY OrderDate ORDER BY OrderDate")
    total_sales_list = []
    for row in cursor:
        total_sales_list.append(row)
    return total_sales_list


def get_currency_rate_data_between_date(cursor, date_from_string, date_to_string):
    cursor.execute(f"SELECT RateDate, MAX(CurrencyRate) FROM {SALES_DATABASE}.{NAME_CURRENCY_TABLE} WHERE RateDate"
                   f" BETWEEN \'{date_from_string}\' AND \'{date_to_string}\' GROUP BY RateDate ORDER BY RateDate")
    rate_data_list = []
    for row in cursor:
        rate_data_list.append(row)
    return rate_data_list
