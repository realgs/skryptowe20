import pyodbc

from currency import get_one_day_currency_rate

SALES_DATABASE = 'AdventureWorks2019'
NAME_SALES_TABLE = 'Sales.SalesOrderHeader'
NAME_CURRENCY_TABLE = 'Sales.CurrencyRateTable'
NAME_DAILY_TURNOVER_TABLE = 'Sales.DailyTurnover'


def connect():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=DESKTOP-IN8O3LQ;'
                          'Database=AdventureWorks2019;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    return cursor


def add_currency_rate_table_to_db(cursor):
    cursor.execute(f"CREATE TABLE {NAME_CURRENCY_TABLE} (RateDate DATETIME NOT NULL, CurrencyRateValue REAL NOT NULL, "
                   f"CurrencyId CHAR(3) NOT NULL, InterpolatedRate BIT NOT NULL)")
    cursor.commit()


def add_daily_turnover_table_to_db(cursor):
    cursor.execute(f"CREATE TABLE {NAME_DAILY_TURNOVER_TABLE} (TurnoverDate DATETIME PRIMARY KEY, "
                   f"TotalTurnover REAL NOT NULL, CurrencyId CHAR(3) NOT NULL )")
    cursor.commit()


def fill_table_currency_rate(cursor, currency_data, currency_id):
    currency_table = __download_currency_table(cursor)
    for i in range(len(currency_data)):
        if not __find_date_in_table(currency_table, currency_data[i]["date"]):
            if currency_data[i]["interpolated"]:
                interpolated = 1
            else:
                interpolated = 0
            __insert_currency_rate(cursor, currency_data[i]['date'], currency_data[i]['mid_rate'], currency_id, interpolated)


def __insert_currency_rate(cursor, rate_date, currency_rate_value, currency_id, is_interpolated):
    if is_interpolated:
        is_interpolated_bit = 1
    else:
        is_interpolated_bit = 0
    cursor.execute(f"INSERT INTO {SALES_DATABASE}.{NAME_CURRENCY_TABLE} (RateDate, CurrencyRateValue, CurrencyId, "
                   f"InterpolatedRate) "
                   f"VALUES (\'{rate_date}\',{currency_rate_value},\'{currency_id}\',"
                   f"{is_interpolated_bit})")
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
                   f" BETWEEN \'{date_from_string}\' AND \'{date_to_string}\' AND CurrencyId = \'PLN\' ORDER BY RateDate")
    rate_data_list = []
    for row in cursor:
        rate_data_list.append(row)
    return rate_data_list


def get_currency_rate_of_day(cursor, date, currency_id):
    result = cursor.execute(f"SELECT CurrencyRateValue FROM {SALES_DATABASE}.{NAME_CURRENCY_TABLE} WHERE RateDate = "
                            f" \'{date}\' AND CurrencyId = \'{currency_id.upper()}\'")
    result_list = []
    for row in result:
        result_list.append(row)
    if not result_list:
        if currency_id == "PLN":
            currency_rate, is_interpolated = get_one_day_currency_rate("USD", str(date)[:10])
            __insert_currency_rate(cursor, str(date)[:10], currency_rate, currency_id, is_interpolated)
        else:
            pln_currency_rate, is_interpolated = get_one_day_currency_rate("USD", str(date)[:10])
            other_currency_rate, is_interpolated = get_one_day_currency_rate(str(currency_id), str(date)[:10])
            currency_rate = pln_currency_rate/other_currency_rate
            __insert_currency_rate(cursor, str(date)[:10], currency_rate, currency_id, is_interpolated)
        return currency_rate
    else:
        return result_list[0][0]
