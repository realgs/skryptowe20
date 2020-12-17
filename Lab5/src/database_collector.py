import sqlite3 as sql
from src import config
from flask import jsonify


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
    sql_exec = f"SELECT rating_date, rate, interpolated " \
               f"FROM CurrencyData " \
               f"WHERE rating_date='{selected_date}'"
    return jsonify(exec_sql_query(sql_exec))


def get_usd_rating_date_range(start_date, end_date):
    sql_exec = f"SELECT rating_date, rate, interpolated " \
               F"FROM currencydata " \
               F"WHERE rating_date BETWEEN '{start_date}' AND '{end_date}'"
    return jsonify(exec_sql_query(sql_exec))


def get_sales(date):
    sql_query = f"SELECT sales_date, rate,PLN_sales, USD_sales " \
                f"FROM DailySales " \
                f"WHERE sales_date='{date}'"
    return jsonify(exec_sql_query(sql_query))


def get_sales_date_range(start_date, end_date):
    sql_query = f"SELECT sales_date, rate,PLN_sales, USD_sales " \
                f"FROM DailySales " \
                f"WHERE sales_date BETWEEN '{start_date}' AND '{end_date}'"
    return jsonify(exec_sql_query(sql_query))
