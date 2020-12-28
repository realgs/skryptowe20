import datetime as dt

from database import SALES_DATABASE, DAILY_SALES_TABLE_NAME, SALES_TABLE_NAME


def count_daily_sales(cursor, date):
    result = __query_answer_to_list(
        cursor.execute(f"""
        SELECT OrderDate, SUM(TotalDue) Total
        FROM {SALES_DATABASE}.{SALES_TABLE_NAME}
        WHERE OrderDate = \'{date}\'
        GROUP BY OrderDate
        ORDER BY OrderDate
        """)
    )

    if len(result) == 0:
        return 0
    else:
        return result[0]


def get_daily_sales(cursor, date, currency):
    daily_sales = __download_daily_sales_table(cursor)
    found, index = __find_date_in_table(daily_sales, date)
    if not found:
        sales = count_daily_sales(cursor, date)
        cursor.execute(f"""
        INSERT INTO {SALES_DATABASE}.{DAILY_SALES_TABLE_NAME} (SaleDate, TotalSale, Currency)
        VALUES (\'{date}\', {sales[1]}, \'{currency}\')
        """)
        cursor.commit()
        return sales[1]
    return daily_sales[index][1]


def __find_date_in_table(data, date_to_find):
    index = -1
    for row in data:
        index += 1
        date = dt.datetime.strptime(str(date_to_find), '%Y-%m-%d')
        if row[0] == date:
            return True, index
    return False, -1


def __download_daily_sales_table(cursor):
    return  __query_answer_to_list(
        cursor.execute(f"""
        SELECT SaleDate, TotalSale, Currency
        FROM {SALES_DATABASE}.{DAILY_SALES_TABLE_NAME}
        ORDER BY SaleDate
        """)
    )


def __query_answer_to_list(query_answer):
    rows = query_answer.fetchall()
    select_list = []
    for row in rows:
        select_list.append([x for x in row])
    return select_list
