"""
Stores methods used to obtain data for API from database.
"""

import pandas as pd

from utils import *


def get_usd_rating(date):
    conn = get_db_connection()
    sql_query = f"""select effectiveDate, USD, interpolated from USDPrices where effectiveDate='{date}'"""
    result = pd.read_sql_query(sql_query, conn)
    return result.to_json(orient="records")


def get_usd_rating_date_range(start_date, end_date):
    conn = get_db_connection()
    sql_query = f"select effectiveDate, USD, interpolated from USDPrices where effectiveDate between '{start_date}' and '{end_date}'"
    result = pd.read_sql_query(sql_query, conn)
    return result.to_json(orient="records")


def get_sales(date):
    conn = get_db_connection()
    sql_query = f"""select DATE, USD, PLN from Sales where DATE='{date}'"""
    result = pd.read_sql_query(sql_query, conn)
    return result.to_json(orient="records")


def get_sales_date_range(start_date, end_date):
    conn = get_db_connection()
    sql_query = f"select DATE, USD, PLN from Sales where DATE between '{start_date}' and '{end_date}'"
    result = pd.read_sql_query(sql_query, conn)
    return result.to_json(orient="records")
