from datetime import datetime, timedelta

import pymysql.cursors
from pymysql import MySQLError, converters

import lab4.rozwiazanie.nbp as nbp

# Connect to the database
conv = converters.conversions.copy()
conv[10] = str
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='classicmodels',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             conv=conv)


def create_table_with_exchange_rates():
    start_date = '2003-1-1'
    end_date = '2005-12-30'
    rates = nbp.get_currency_rates_from_date_range('usd', start_date, end_date)
    merged_list = [[rates[1][i], round(rates[0][i], 2)] for i in range(0, len(rates[0]))]
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS usd_pln (date DATE UNIQUE, usd REAL DEFAULT 1 , pln REAL)"
            cursor.execute(sql)
        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO usd_pln (date, pln) VALUES (%s, %s)"
            cursor.executemany(sql, merged_list)
        connection.commit()

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


def get_sales_list_from_db(start_date, end_date):
    sd = datetime.strptime(start_date, "%Y-%m-%d").date()
    ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    all_dates = [str(sd + timedelta(days=i)) for i in range((ed - sd).days)]

    try:
        with connection.cursor() as cursor:
            sql = """SELECT o.orderDate, ROUND(SUM(od.quantityOrdered * (od.priceEach * usdpl.pln)),2) cenapl, ROUND(SUM(od.quantityOrdered * (od.priceEach * usdpl.usd) ),2) cenausd
            FROM orders o
            JOIN orderdetails od ON o.orderNumber = od.orderNumber
            JOIN usd_pln usdpl ON o.orderDate = usdpl.date
            WHERE o.orderDate BETWEEN %s AND %s
            GROUP BY o.orderDate"""
            cursor.execute(sql, (start_date, end_date))
            rows = cursor.fetchall()
            result = [[], [], []]
            for row in rows:
                result[0].append(row['orderDate'])
                result[1].append(row['cenausd'])
                result[2].append(row['cenapl'])

            for i in range(len(all_dates)):
                if i >= len(result[0]) or all_dates[i] != result[0][i]:
                    result[0].insert(i, all_dates[i])
                    result[1].insert(i, 0)
                    result[2].insert(i, 0)

            return result

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))

