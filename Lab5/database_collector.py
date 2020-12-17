import os

from flask import jsonify

import config
import sqlite3 as sql


def connect():
    return sql.connect(config.CALC_DATABASE_FILENAME)


def exec_sql_query(query):
    c = connect()
    cursor = c.cursor()
    cursor.execute(query)
    rating = cursor.fetchall()
    c.close()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
            for row in rating]
    c.close()
    return data


def get_usd_rating(selected_date):
    sql_exec = f"Select rating_date, rate, interpolated " \
               f"from CurrencyData " \
               f"where rating_date='{selected_date}'"
    return jsonify(exec_sql_query(sql_exec))


def get_usd_rating_date_range(start_date, end_date):
    sql_exec = f"select rating_date, rate, interpolated " \
               f"from CurrencyData " \
               f"where rating_date between '{start_date}' and '{end_date}'"
    return jsonify(exec_sql_query(sql_exec))


def get_sales(date):
    sql_query = f"select sales_date, rate,PLN_sales, USD_sales " \
                f"from DailySales " \
                f"where sales_date='{date}'"
    return jsonify(exec_sql_query(sql_query))


def get_sales_date_range(start_date, end_date):
    sql_query = f"select sales_date, rate,PLN_sales, USD_sales " \
                f"from DailySales " \
                f"where sales_date between '{start_date}' and '{end_date}'"
    return jsonify(exec_sql_query(sql_query))
