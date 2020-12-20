from datetime import datetime, timedelta

import pymysql.cursors
from pymysql import MySQLError, converters

import lab5.nbp as nbp

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
    merged_list = [[rates[1][i], round(rates[0][i], 2), [rates[2][i]]] for i in range(0, len(rates[0]))]
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS usd_pln (date DATE UNIQUE, usd REAL DEFAULT 1 , pln REAL, interpolated TINYINT(1))"
            cursor.execute(sql)
        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO usd_pln (date, pln, interpolated) VALUES (%s, %s, %s)"
            cursor.executemany(sql, merged_list)
        connection.commit()

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


def create_sales_table():
    start_date = '2003-1-1'
    end_date = '2004-07-07'

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
            result = []
            for row in rows:
                result.append([row['orderDate'], row['cenausd'], row['cenapl']])

            for i in range(len(all_dates)):
                if i >= len(result) or all_dates[i] != result[i][0]:
                    result.insert(i, [all_dates[i], 0, 0])

        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS daily_sales_summary (date DATE UNIQUE, original_usd REAL, converted_pln REAL)"
            cursor.execute(sql)
        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO daily_sales_summary (date, original_usd, converted_pln) VALUES (%s, %s, %s)"
            cursor.executemany(sql, result)
        connection.commit()

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


def get_usd_exchange_rate_for_one_day(date):

    try:
        with connection.cursor() as cursor:
            sql = """SELECT usd_pln.date date, ROUND(usd_pln.pln,2) cenapl, usd_pln.interpolated interpolated
            FROM usd_pln
            WHERE usd_pln.date = %s"""
            cursor.execute(sql, date)
            row = cursor.fetchone()
            if row is None:
                return None
            result = {
                "date": row['date'],
                "rate": row['cenapl'],
                "interpolated": row['interpolated'],
            }

            return result

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


def get_usd_exchange_rate_for_days_range(start_date, end_date):

    try:
        with connection.cursor() as cursor:
            sql = """SELECT usd_pln.date date, ROUND(usd_pln.pln,2) cenapl, usd_pln.interpolated interpolated
            FROM usd_pln
            WHERE usd_pln.date BETWEEN %s AND %s
            """
            cursor.execute(sql, (start_date, end_date))
            rows = cursor.fetchall()
            if rows is None:
                return None

            result = []
            for row in rows:
                result.append({
                    "date": row['date'],
                    "rate": row['cenapl'],
                    "interpolated": row['interpolated'],
                })
            return result

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


def get_usd_exchange_min_date():
    try:
        with connection.cursor() as cursor:
            sql = """SELECT usd_pln.date date
            FROM usd_pln
            ORDER BY usd_pln.date           
            """
            cursor.execute(sql)
            return cursor.fetchone()['date']

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


def get_usd_exchange_max_date():
    try:
        with connection.cursor() as cursor:
            sql = """SELECT usd_pln.date date
            FROM usd_pln
            ORDER BY usd_pln.date DESC          
            """
            cursor.execute(sql)
            return cursor.fetchone()['date']

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


def get_sales_sum_for_day_x(date):

    try:
        with connection.cursor() as cursor:
            sql = """SELECT date, original_usd, converted_pln
            FROM daily_sales_summary
            WHERE date = %s"""
            cursor.execute(sql, date)
            row = cursor.fetchone()
            if row is None:
                return None

            return row

    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))