from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TransactionLogs(Base):

    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    order_num = Column(Integer)
    quantity = Column(Integer)
    price_each = Column(Float)
    orderline_num = Column(Integer)
    sales = Column(Float)
    order_date = Column(Date)
    status = Column(String)
    qtr_id = Column(Integer)
    month = Column(Integer)
    year_id = Column(Integer)
    product_line = Column(String)
    msrp = Column(Integer)
    product_code = Column(String)
    customer_name = Column(String)
    phone = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    city = Column(String)
    state = Column(String)
    postalcode = Column(String)
    country = Column(String)
    territory = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    deal_size = Column(String)