import pyodbc

SALES_DATABASE = 'AdventureWorks2019'
NAME_SALES_TABLE = 'Sales.SalesOrderHeader'
NAME_CURRENCY_TABLE = 'Sales.UsdRate'
NAME_DAILY_TURNOVER_TABLE = 'Sales.DailyTurnover'


def connect():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=DESKTOP-IN8O3LQ;'
                          'Database=AdventureWorks2019;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    return cursor


def add_usd_rate_table_to_db(cursor):
    cursor.execute(f"CREATE TABLE {NAME_CURRENCY_TABLE} (RateDate DATETIME PRIMARY KEY, CurrencyRate REAL NOT NULL, "
                   f"InterpolatedRate BIT NOT NULL)")
    cursor.commit()


def add_daily_turnover_table_to_db(cursor):
    cursor.execute(f"CREATE TABLE {NAME_DAILY_TURNOVER_TABLE} (TurnoverDate DATETIME PRIMARY KEY, "
                   f"TotalTurnover REAL NOT NULL, Rate CHAR(3) NOT NULL )")
    cursor.commit()


def fill_table_usd_rate(cursor, currency_data):
    currency_table = __download_currency_table(cursor)
    for i in range(len(currency_data)):
        if not __find_date_in_table(currency_table, currency_data[i]["date"]):
            if currency_data[i]["interpolated"]:
                interpolated = 1
            else:
                interpolated = 0
            cursor.execute(f"INSERT INTO {SALES_DATABASE}.{NAME_CURRENCY_TABLE} (RateDate, CurrencyRate, InterpolatedRate) VALUES ("
                           f"\'{currency_data[i]['date']}\',{currency_data[i]['mid_rate']},{interpolated})")
            cursor.commit()


def __find_date_in_table(data, date_to_find):
    return date_to_find in data


def __download_currency_table(cursor):
    cursor.execute(f"SELECT RateDate FROM {SALES_DATABASE}.{NAME_CURRENCY_TABLE} ORDER BY RateDate")
    select_list = []
    for row in cursor:
        select_list.append(row[0])
    return select_list


def get_currency_rate_data_between_date(cursor, date_from_string, date_to_string):
    cursor.execute(f"SELECT * FROM {SALES_DATABASE}.{NAME_CURRENCY_TABLE} WHERE RateDate"
                   f" BETWEEN \'{date_from_string}\' AND \'{date_to_string}\' ORDER BY RateDate")
    rate_data_list = []
    for row in cursor:
        rate_data_list.append(row)
    return rate_data_list


def get_currency_rate_of_day(cursor, date):
    result = cursor.execute(f"SELECT CurrencyRate FROM {SALES_DATABASE}.{NAME_CURRENCY_TABLE} WHERE RateDate = "
                   f" \'{date}\'")
    result_list = []
    for row in result:
        result_list.append(row)
    return result_list
