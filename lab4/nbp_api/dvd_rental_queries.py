from decimal import Decimal

import sqlalchemy
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import api_usage

DB_URI = "postgres://postgres:bazman@localhost:5432/dvdrental"


def create_usd_eur_price_graph(days):
    # connect
    engine = sqlalchemy.create_engine(DB_URI)
    conn = engine.connect()
    Base = automap_base()
    Base.prepare(conn, reflect=True)
    Session = sessionmaker(bind=conn)
    session = Session()
    # prepare data
    payments_table = session.query(Base.classes.payment).all()
    exchange_rate_table = session.query(Base.classes.exchange_rate).all()
    # create graph
    dates = []
    values_pln = []
    values_usd = []
    for i in range(days):
        date = datetime.date.today()-datetime.timedelta(days=days - i)
        dates.append(date)
        ids = find_all_payment_ids_with_date(payments_table, date)
        values_usd.append(0)
        for j in range(len(ids)):
            values_usd[i] += payments_table[ids[j]].amount
        exchange_rate_id = find_exchange_rate_id_with_date(exchange_rate_table, date)
        values_pln.append(values_usd[i] * Decimal(exchange_rate_table[exchange_rate_id].usd_to_pln))
    fig, ax = plt.subplots()
    plt.plot(dates, values_pln, color='red')
    plt.plot(dates, values_usd, color='green')
    pln_patch = mpatches.Patch(color='red', label='Total income in PLN')
    usd_patch = mpatches.Patch(color='green', label='Total income in USD')
    plt.legend(handles=[pln_patch, usd_patch])
    plt.xlabel('Date')
    plt.ylabel('Total income')
    plt.title('Total income from last {} days in USD and PLN'.format(days))
    plt.xticks(dates[::int(days/20)])
    fig.autofmt_xdate()
    plt.show()


def find_exchange_rate_id_with_date(data, date):
    # when working with more data it probably would be better to use
    # binary search, as dates are sorted, but this one is fast enough for its purpose
    for i in range(len(data)):
        if data[i].date.strftime("%m/%d/%Y") == date.strftime("%m/%d/%Y"):
            return i
    return -1


def find_all_payment_ids_with_date(data, date):
    # payments were not sorted by dates
    ids = []
    for i in range(len(data)):
        if data[i].payment_date.strftime("%m/%d/%Y") == date.strftime("%m/%d/%Y"):
            ids.append(i)
    return ids


create_usd_eur_price_graph(183)
