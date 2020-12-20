import os

from sqlalchemy.sql.functions import sum
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

Base = automap_base()
engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'sales.db'))
Base.prepare(engine, reflect=True)

Rates = Base.classes.rates
Sales = Base.classes.invoices

session = Session(engine)
# "RateDate" "Rate" "Code" "Interpolated"


def get_todays_date(code):
    date = session.query(func.max(Rates.RateDate)).first()[0]
    return date


def get_rate(date, code):
    rate, ipd = session.query(Rates.Rate, Rates.Interpolated).filter_by(Code=code, RateDate=date).first()
    return rate, ipd


def get_rates_ipd(date_from, date_to, code):
    data = session.query(Rates.RateDate,
                         Rates.Rate,
                         Rates.Interpolated).filter(and_(Rates.Code == code,
                                                         Rates.RateDate >= date_from,
                                                         Rates.RateDate <= date_to)).all()
    return data


def get_sales(date_from, date_to):
    data = session.query(Sales.InvoiceDate, sum(Sales.Total)).group_by(Sales.InvoiceDate).all()
    return data


get_sales('2009-01-01', '2009-01-31')
