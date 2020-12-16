"""
Stores methods used to calculate orders value daily with data stored in database.
"""

import pandas as pd

from utils import get_db_connection


def get_orders_value_daily(start_date, end_date):
    conn = get_db_connection()

    orders_value_daily_sql_query = """
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

    statement = orders_value_daily_sql_query.format(date_format=DATE_FORMAT, start_date=start_date, end_date=end_date)

    query = pd.read_sql_query(statement, conn)
    orders_value_data = pd.DataFrame(query).set_index('DATE')

    return orders_value_data
