"""
Script to populate database with currency and sales data.
"""
import pandas as pd
from ccy_data import get_complete_usd_daily_ex_rates
from conf import PATH_TO_DB
from sales_data import get_orders_value_daily
from utils import DATA_DATE_RANGE_START, DATA_DATE_RANGE_END, get_db_connection

USD_EX_RATES_TABLE_NAME = 'USDPrices'
SALES_TABLE_NAME = 'Sales'


def add_table(conn, table_data: pd.DataFrame, table_name):
    table_data.to_sql(table_name, conn, if_exists='replace')


db_conn = get_db_connection(PATH_TO_DB)

usd_daily_ex_rates_df = get_complete_usd_daily_ex_rates(DATA_DATE_RANGE_START, DATA_DATE_RANGE_END)
add_table(db_conn, usd_daily_ex_rates_df, USD_EX_RATES_TABLE_NAME)

orders_value_daily_data = get_orders_value_daily(DATA_DATE_RANGE_START, DATA_DATE_RANGE_END)
add_table(db_conn, orders_value_daily_data, SALES_TABLE_NAME)
