from currency_rate import CurrencyRateTable
from transaction_logs import TransactionLogs
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:admin@localhost/transaction_log')

session = sessionmaker(engine)
# transaction_logs = session.query(TransactionLogs).filter_by(id = "")