from datetime import datetime
import datetime as dt
import requests
from datetime import date

from connectDB import SALES_DATABASE, NAME_DAILY_TURNOVER_TABLE, NAME_SALES_TABLE


def count_daily_turnover(cursor, date):
    result = database_select_to_list(cursor.execute(
        f"SELECT OrderDate, SUM(TotalDue) Total FROM {SALES_DATABASE}.{NAME_SALES_TABLE} WHERE OrderDate = \'{date}\' "
        f"GROUP BY OrderDate ORDER BY OrderDate"))
    if len(result) == 0:
        return 0
    else:
        return result[0]


def get_daily_turnover(cursor, date):
    daily_turnover_in_db = download_daily_turnover_table(cursor)
    is_find, index = find_date_in_table(daily_turnover_in_db, date)
    if not is_find:
        turnover = count_daily_turnover(cursor, date)
        cursor.execute(f"INSERT INTO {SALES_DATABASE}.{NAME_DAILY_TURNOVER_TABLE} "
                       f"(TurnoverDate, TotalTurnover, Rate) "
                       f"VALUES (\'{date}\',{turnover[1]},\'USD\')")
        cursor.commit()
        return turnover[1]
    return daily_turnover_in_db[index][1]


def find_date_in_table(data, date_to_find):
    index = -1
    for row in data:
        index += 1
        date2 = date_to_small_string(date_to_find)
        if row[0] == date2:
            return True, index
    return False, -1


def date_to_small_string(string_date):
    return dt.datetime.strptime(str(string_date), '%Y-%m-%d')


def download_daily_turnover_table(cursor):
    return database_select_to_list(cursor.execute(f"SELECT TurnoverDate, TotalTurnover, Rate FROM {SALES_DATABASE}.{NAME_DAILY_TURNOVER_TABLE} "
                          f"ORDER BY TurnoverDate"))


def database_select_to_list(cursor_result):
    rows = cursor_result.fetchall()
    select_list = []
    for row in rows:
        select_list.append([x for x in row])
    return select_list
