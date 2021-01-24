import sqlite3
from datetime import timedelta

DATABASE = 'database_files/Northwind.sqlite'

WRONG_DATE_RANGE = 416
NO_DATA_FOUND = 404


def getSaleFromDatabase(saleDate):
    start_date = saleDate - timedelta(seconds=1)
    end_date = saleDate + timedelta(hours=23, minutes=59, seconds=59)
    return getDataFromPeriod(start_date, end_date)


def getSalesFromDatabase(start, end):
    start_date = start - timedelta(seconds=1)
    end_date = end + timedelta(hours=23, minutes=59, seconds=59)

    if start_date > end_date:
        return WRONG_DATE_RANGE
    return getDataFromPeriod(start_date, end_date)


def getDataFromPeriod(start_date, end_date):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"""
      SELECT
            strftime('%Y-%m-%d',  date(OrderDate)),
            sum(UnitPrice * Quantity)
       FROM
            [Order]
                JOIN OrderDetail ON [Order].Id = OrderDetail.OrderId
       WHERE
            OrderDate BETWEEN '{start_date}' AND '{end_date}'
       GROUP BY date(OrderDate)
       """)
    data = cursor.fetchall()
    sales = {}
    for sale in data:
        sales[sale[0]] = sale[1]
    if sales == {}:
        return NO_DATA_FOUND
    return sales
    