import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

from currency_data import get_currencies_data

USD_PRICES_TABLE_NAME = 'USDPrices'
DATE_FORMAT = "%Y-%m-%d"


def get_complete_usd_to_pln_data(start_date, end_date):
    catchup = (end_date - start_date).days + 1
    usd_to_pln_daily = get_currencies_data(['USD'], catchup, end_date)

    ref_price = usd_to_pln_daily.loc[usd_to_pln_daily.index[0]]['USD']

    for single_date in ((start_date + timedelta(days=i)).strftime(DATE_FORMAT) for i in range(catchup)):
        if single_date not in usd_to_pln_daily.index:
            usd_to_pln_daily.loc[single_date] = ref_price
        else:
            ref_price = usd_to_pln_daily.loc[single_date]['USD']
    usd_to_pln_daily.sort_index(inplace=True)

    return usd_to_pln_daily


def add_usd_to_pln_table(conn, usd_to_pln_daily: pd.DataFrame):
    usd_to_pln_daily.to_sql(USD_PRICES_TABLE_NAME, conn, if_exists='replace')


def get_db_connection(database_name):
    return sqlite3.connect(database_name)


def draw_chart(data: pd.DataFrame):
    data.plot(title="Orders value daily", xlabel="Date", ylabel="Value")
    plt.legend().set_title("Currency")
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.show()


def get_orders_value_daily_data(start_date, end_date):
    statement = f"""
       select strftime('%Y-%m-%d',  date(OrderDate)) "DATE", UnitPrice * Quantity  "USD", UnitPrice * Quantity * USD "PLN"
       from [Order] join OrderDetail on [Order].Id=OrderDetail.OrderId join USDPrices on strftime('%Y-%m-%d',  date(OrderDate)) = effectiveDate
       where OrderDate between '{start_date.strftime(DATE_FORMAT)}' and '{end_date.strftime("%Y-%m-%d")}' 
       """

    query = pd.read_sql_query(statement, db_conn)
    orders_value_data = pd.DataFrame(query).set_index('DATE')

    return orders_value_data


if __name__ == '__main__':
    strt = datetime(2013, 12, 1)
    end = datetime(2014, 1, 1)

    add_df = get_complete_usd_to_pln_data(strt, end)

    db_conn = get_db_connection('database_files/Northwind_small.db')

    add_usd_to_pln_table(db_conn, add_df)

    orders_value_daily_data = get_orders_value_daily_data(strt, end)
    draw_chart(orders_value_daily_data)
