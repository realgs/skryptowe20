import psycopg2
import transaction_logs as tl
from numpy import genfromtxt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

csv_file_name = 'C:/Users/mielcare/Downloads/sales_data_sample.csv'


def load_data(file_name):
    data = genfromtxt(file_name,dtype=str, delimiter=',', skip_header=1, invalid_raise=False)
    return data.tolist()


def init_db():

    engine = create_engine('postgresql+psycopg2://postgres:admin@localhost/transaction_log')
    tl.Base.metadata.create_all(engine)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    data = load_data(csv_file_name)
    try:
        for i in data:
            record = tl.TransactionLogs(**{
                'order_num': int(i[0]),
                'quantity': int(i[1]),
                'price_each': float(i[2]),
                'orderline_num': int(i[3]),
                'sales': float(i[4]),
                'order_date': i[5],
                'status': i[6],
                'qtr_id': int(i[7]),
                'month': int(i[8]),
                'year_id': int(i[9]),
                'product_line': i[10],
                'msrp': int(i[11]),
                'product_code': i[12],
                'customer_name': i[13],
                'phone': i[14],
                'address_line1': i[15],
                'address_line2': i[16],
                'city': i[17],
                'state': i[18],
                'postalcode': i[19],
                'country': i[20],
                'territory': i[21],
                'last_name': i[22],
                'first_name': i[23],
                'deal_size': i[24]
             })
            s.add(record)
        s.commit()
    except:
        s.rollback()
    finally:
        s.close()


init_db()