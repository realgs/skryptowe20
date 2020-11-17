import sqlalchemy
import psycopg2
from faker import Faker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

DB_URI = "postgres://postgres:bazman@localhost:5432/dvdrental"
fake = Faker('pl_PL')


# my database contained only payments from between a few months, so I had to recreate them with new random values
def main():
    engine = sqlalchemy.create_engine(DB_URI)
    conn = engine.connect()
    Base = automap_base()
    Base.prepare(conn, reflect=True)
    Session = sessionmaker(bind=conn)
    session = Session()
    table = Base.classes.payment
    rows = session.query(table)
    for row in rows:
        row.payment_date = fake.date_between(start_date="-3y", end_date="today")
    session.commit()


main()
