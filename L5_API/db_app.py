import os

from sqlalchemy.sql.functions import sum
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

Base = automap_base()
engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'sales.db' + '?check_same_thread=False'))
Base.prepare(engine, reflect=True)

Rates = Base.classes.rates
Sales = Base.classes.invoices

session = Session(engine)


def get_last_date(code):
    return session.query(func.max(Rates.RateDate)).filter_by(Code=code.upper()).first()[0]


def get_rate(code, date):
    result = session.query(Rates).filter_by(RateDate=date, Code=code.upper()).first()
    return result.Rate, result.Interpolated


def get_rates_ipd(code, date_from, date_to):
    data = session.query(Rates).filter(and_(Rates.Code == code.upper(),
                                            Rates.RateDate >= date_from,
                                            Rates.RateDate <= date_to)).all()
    data = [{"date": d.RateDate, "rate": d.Rate, "ipd": d.Interpolated} for d in data]
    return data


def get_sales(date_from, date_to):
    data = session.query(Sales.InvoiceDate, sum(Sales.Total)).group_by(Sales.InvoiceDate).all()
    return data


def get_limits(code):
    date_max = session.query(func.max(Rates.RateDate)).filter_by(Code=code.upper()).first()[0]
    date_min = session.query(func.min(Rates.RateDate)).filter_by(Code=code.upper()).first()[0]
    return date_min, date_max