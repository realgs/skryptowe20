import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker

from currency_data import get_currencies_daily_ex_rates

USD_ISO_CODE = 'USD'
USD_EX_RATES_TABLE_NAME = 'USDPrices'
PATH_TO_DB = 'database_files/Northwind.db'
ORDERS_VALUE_DAILY_SQL_QUERY = """
   select 
        strftime('{date_format}',  date(OrderDate)) "DATE", 
        sum(UnitPrice * Quantity)  "USD", 
        sum(UnitPrice * Quantity * USD) "PLN"
   from 
        [Order] 
            join OrderDetail on [Order].Id=OrderDetail.OrderId 
            join USDPrices on strftime('%Y-%m-%d',  date(OrderDate)) = effectiveDate
   where 
        OrderDate between '{start_date}' and '{end_date}' 
        
   group by date(OrderDate)
   """
DATE_FORMAT = "%Y-%m-%d"


def complete_usd_daily_ex_rates(usd_daily_ex_rates, start_date, end_date):
    ref_price = usd_daily_ex_rates.loc[usd_daily_ex_rates.index[0]][USD_ISO_CODE]
    for date in ((start_date + timedelta(days=i)) for i in range((end_date - start_date).days)):
        date = date.strftime(DATE_FORMAT)

        if date not in usd_daily_ex_rates.index:
            usd_daily_ex_rates.loc[date] = ref_price
        else:
            ref_price = usd_daily_ex_rates.loc[date][USD_ISO_CODE]
    usd_daily_ex_rates.sort_index(inplace=True)

    return usd_daily_ex_rates


def get_complete_usd_daily_ex_rates(start_date, end_date):
    usd_daily_ex_rates = get_currencies_daily_ex_rates([USD_ISO_CODE], start_date, end_date)
    return complete_usd_daily_ex_rates(usd_daily_ex_rates, start_date, end_date)


def add_table(conn, usd_to_pln_daily: pd.DataFrame):
    usd_to_pln_daily.to_sql(USD_EX_RATES_TABLE_NAME, conn, if_exists='replace')


def get_db_connection(database_name):
    return sqlite3.connect(database_name)


def draw_chart(data: pd.DataFrame):
    data.plot(title="Orders value daily", xlabel="Date", ylabel="Value", figsize=(25, 6), rot=30)
    plt.legend().set_title("Currency")
    plt.gcf().subplots_adjust(bottom=0.2)

    plt.savefig("orders_value_daily.svg")


def get_orders_value_daily(start_date, end_date):
    statement = ORDERS_VALUE_DAILY_SQL_QUERY.format(date_format=DATE_FORMAT, start_date=start_date, end_date=end_date)

    query = pd.read_sql_query(statement, db_conn)
    orders_value_data = pd.DataFrame(query).set_index('DATE')

    return orders_value_data


if __name__ == '__main__':
    strt = datetime(2013, 1, 1)
    end = datetime(2015, 1, 1)

    usd_daily_ex_rates_df = get_complete_usd_daily_ex_rates(strt, end)

    db_conn = get_db_connection(PATH_TO_DB)

    add_table(db_conn, usd_daily_ex_rates_df)

    orders_value_daily_data = get_orders_value_daily(strt, end)
    draw_chart(orders_value_daily_data)
