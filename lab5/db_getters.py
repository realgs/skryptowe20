from datetime import datetime
from database import connect
import pandas as pd

DATE_FORMAT = '%Y-%m-%d'


def get_usd_prices_from_date(date):
    connection = connect()
    date = datetime.strptime(date, DATE_FORMAT)
    query = f"""SELECT RateDate, Exchange, Interpolated 
                FROM UsdPlnExchangeRate 
                WHERE RateDate='{date}'"""
    result = pd.read_sql_query(query, connection)
    return result.to_dict(orient="records")


def get_usd_prices_between_dates(start_date, end_date):
    connection = connect()
    start_date =  datetime.strptime(start_date, DATE_FORMAT)
    end_date =  datetime.strptime(end_date, DATE_FORMAT)
    query = f"""SELECT RateDate, Exchange, Interpolated 
                   FROM UsdPlnExchangeRate 
                   WHERE RateDate BETWEEN '{start_date}' AND'{end_date}'"""
    result = pd.read_sql_query(query, connection)
    return result.to_dict(orient="records")


def get_sales_from_day(date):
    connection = connect()
    query = f"""SELECT 
                    OrderDate,
                    SUM(UnitPrice * Quantity*(1-Discount)) AS UsdPrice,
                    MAX(RateDate) AS RateDate, 
                    Exchange,
                    SUM(UnitPrice * Quantity*(1-Discount)) * Exchange AS PlnPrice
                    FROM "Order Details" NATURAL JOIN Orders JOIN UsdPlnExchangeRate ON OrderDate >= RateDate
                    WHERE OrderDate = '{date}'"""
    result = pd.read_sql_query(query, connection)
    return result.to_dict(orient="records")


def get_sales_between_days(start_date, end_date):
    connection = connect()
    query = f"""SELECT 
                    OrderDate,
                    SUM(UnitPrice * Quantity*(1-Discount)) AS UsdPrice,
                    MAX(RateDate) AS RateDate, 
                    Exchange,
                    SUM(UnitPrice * Quantity*(1-Discount)) * Exchange AS PlnPrice
                    FROM "Order Details" NATURAL JOIN Orders JOIN UsdPlnExchangeRate ON OrderDate >= RateDate
                    GROUP BY OrderDate
                    HAVING OrderDate BETWEEN '{start_date}' AND '{end_date}'"""
    result = pd.read_sql_query(query, connection)
    return result.to_dict(orient="records")


if __name__ == '__main__':
    res = get_usd_prices_from_date(datetime.strptime("2018-07-13", DATE_FORMAT))
    print(res)
    res = get_usd_prices_between_dates(datetime.strptime("2018-07-13", DATE_FORMAT),
                                       datetime.strptime("2018-07-15", DATE_FORMAT))
    print(res)
    res = get_sales_from_day('2018-07-08')
    print(res)
    res = get_sales_between_days('2018-07-12', '2018-07-15')
    print(res)
