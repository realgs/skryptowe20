import os

from sqlalchemy.sql.functions import sum
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from L5_API.constants import DATE_FORMAT

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
    data = session.query(Sales.InvoiceDate,
                         sum(Sales.Total * 100)/100,
                         sum(Sales.Total_pln * 100)/100).group_by(Sales.InvoiceDate)
    data = data.filter(and_(Sales.InvoiceDate >= date_from,
                            Sales.InvoiceDate <= date_to)).all()
    data = [{"date": d[0].strftime(DATE_FORMAT), "total_usd": float(d[1]), "total_pln": float(d[2])} for d in data]
    return data


def get_rates_limits(code):
    date_max = session.query(func.max(Rates.RateDate)).filter_by(Code=code.upper()).first()[0]
    date_min = session.query(func.min(Rates.RateDate)).filter_by(Code=code.upper()).first()[0]
    return date_min, date_max


def get_sales_limits():
    date_max = session.query(func.max(Sales.InvoiceDate)).first()[0].strftime(DATE_FORMAT)
    date_min = session.query(func.min(Sales.InvoiceDate)).first()[0].strftime(DATE_FORMAT)
    return date_min, date_max
