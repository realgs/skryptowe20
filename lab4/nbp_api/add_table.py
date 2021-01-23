import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, Float, DateTime, insert
import datetime
import api_usage


DB_URI = "postgres://postgres:bazman@localhost:5432/dvdrental"


def create_exchange_rate_table_with_data():
    days = 1200
    # connect
    engine = sqlalchemy.create_engine(DB_URI)
    conn = engine.connect()
    meta = MetaData()
    # create table
    exchange_rate = Table(
        'exchange_rate', meta,
        Column('exchange_rate_id', Integer, primary_key=True),
        Column('usd_to_pln', Float),
        Column('date', DateTime),
    )
    meta.create_all(conn)
    # insert rows
    usd_data = api_usage.currency_from_last_x_days("USD", days)
    data = []
    for i in range(days):
        date = datetime.date.today()-datetime.timedelta(days=days - i)
        index = find_usd_data_id_with_date(usd_data, date)
        j = 0
        while index == -1:
            j += 1
            index = find_usd_data_id_with_date(usd_data, date - datetime.timedelta(days=j))
            if j > 7:  # if w checked more than seven days we can assume we will never find date in data
                break
        if index == -1:
            data.append({'usd_to_pln': 0, 'date': date})
        else:
            data.append({'usd_to_pln': usd_data['rates'][index]['mid'], 'date': date})
    insert_expr = insert(meta.tables['exchange_rate'], values=data)
    conn.execute(insert_expr)


def find_usd_data_id_with_date(data, date):
    # when working with more data it probably would be better to use
    # binary search, as dates are sorted, but this one is fast enough for its purpose
    for i in range(len(data['rates'])):
        if data['rates'][i]['effectiveDate'] == str(date):
            return i
    return -1


create_exchange_rate_table_with_data()
