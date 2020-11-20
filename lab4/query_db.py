from currency_rate import CurrencyRateTable
from transaction_logs import TransactionLogs
from sqlalchemy.orm import sessionmaker, session, Query
from sqlalchemy import create_engine
from sqlalchemy import asc

engine = create_engine('postgresql+psycopg2://postgres:admin@localhost/transaction_log')

Session = sessionmaker(engine)
session = Session()


def get_transaction_logs():
    logs = session.query(TransactionLogs).filter(TransactionLogs.order_date > '2004-05-06').filter(
        TransactionLogs.order_date < '2004-10-07').order_by(asc('order_date'))
    return logs


def get_currency_rates():
    rates = session.query(CurrencyRateTable).filter(CurrencyRateTable.date > '2004-05-06').filter(
        CurrencyRateTable.date < '2004-10-07')
    return rates
