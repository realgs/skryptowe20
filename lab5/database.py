import pyodbc
import currency_api

SALES_DATABASE = 'AdventureWorks2019'
SALES_TABLE_NAME = 'Sales.SalesOrderHeader'
CURRENCY_TABLE_NAME = 'Sales.CurrencyRatesTable'
DAILY_SALES_TABLE_NAME = 'Sales.DailySalesTable'
SERVER = 'DESKTOP-1A5C2CG'


def connect():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          f'Server={SERVER};'
                          f'Database={SALES_DATABASE};'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    return cursor


def create_currency_table(cursor):
    cursor.execute(f'''
    CREATE TABLE {CURRENCY_TABLE_NAME} (
        QuotationDate DATETIME NOT NULL,
        CurrencyValue REAL NOT NULL,
        CurrencyId CHAR(3) NOT NULL,
        Interpolated BIT NOT NULL
        )
    ''')


def fill_currency_table(cursor, data_list, currency_id):
    currency_table = __download_currency_table(cursor)
    for data in data_list:
        if not __find_date(currency_table, data['date']):
            if data['interpolated']:
                interpolated = 1
            else:
                interpolated = 0
            __insert_currency_rate(cursor, data['date'], data['mid'], currency_id, interpolated)


def get_currency_rate_data_between_date(cursor, date_from, date_to):
    cursor.execute(f"""
    SELECT * 
    FROM {SALES_DATABASE}.{CURRENCY_TABLE_NAME}
    WHERE QuotationDate BETWEEN \'{date_from}\' AND \'{date_to}\'
    ORDER BY QuotationDate
    """)
    data_list = []
    for row in cursor:
        data_list.append(row)
    return data_list


def __download_currency_table(cursor):
    cursor.execute(f'''
    SELECT QuotationDate 
    FROM {SALES_DATABASE}.{CURRENCY_TABLE_NAME}
    ORDER BY QuotationDate
    ''')
    list = []
    for row in cursor:
        print(row)
        list.append(row[0])
    return list


def __find_date(table, date):
    return date in table


def __insert_currency_rate(cursor, date, rate, currency_id, is_interpolated):
    if is_interpolated:
        inter = 1
    else:
        inter = 0
    cursor.execute(f"""
    INSERT INTO {SALES_DATABASE}.{CURRENCY_TABLE_NAME} (QuotationDate, CurrencyValue, CurrencyId, Interpolated)
    VALUES (\'{date}\', {rate}, \'{currency_id}\', {inter})
    """)
    cursor.commit()

def create_daily_sales_table(cursor):
    cursor.execute(f'''
    CREATE TABLE {DAILY_SALES_TABLE_NAME} (
    SaleDate DATETIME PRIMARY KEY,
    TotalSale REAL NOT NULL,
    Currency CHAR(3) NOT NULL
    )
    ''')
    cursor.commit()

def get_currency_rate_of_day(cursor, date, currency):
    result = cursor.execute(f"""
    SELECT CurrencyValue
    FROM {SALES_DATABASE}.{CURRENCY_TABLE_NAME}
    WHERE QuotationDate = \'{date}\' AND CurrencyId = \'{currency.upper()}\'
    """)

    result_list = []
    for row in result:
        result_list.append(row)
    if not result_list:
        if currency == "PLN":
            currency_rate, interpolated = currency_api.get_one_day_currency_rate("USD", str(date)[:10])
            __insert_currency_rate(cursor, str(date)[:10], currency_rate, currency, interpolated)
        else:
            pln_currency_rate, interpolated = currency_api.get_one_day_currency_rate("USD", str(date)[:10])
            other_currency_rate, interpolated = currency_api.get_one_day_currency_rate(str(currency), str(date)[:10])
            currency_rate = pln_currency_rate/other_currency_rate
            __insert_currency_rate(cursor, str(date)[:10], currency_rate, currency, interpolated)
        return currency_rate
    else:
        return result_list[0][0]