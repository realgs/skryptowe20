from sqlalchemy import Column, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CurrencyRateTable(Base):
    __tablename__ = 'currency_rate'
    date = Column(Date, primary_key=True, nullable=False)
    rate = Column(Float)