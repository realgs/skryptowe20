import sqlite3
from constants import DATABASE_PATH
from web_data import RatesWrapper

def connect_to_database():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn.cursor(), conn

def create_table(cursor, currency):
    querry = f"DROP TABLE IF EXISTS {currency}Rates;"
    cursor.execute(querry)
    querry = f"""
    CREATE TABLE [{currency}Rates] (
        [EffectiveDate] TEXT,
        [Mid] REAL,
        [Interpolated] INTEGER
    );
    """
    cursor.execute(querry)

def populate_table(cursor, wrapper):
    for rate in wrapper.rates:
        querry = f"""
        INSERT INTO [{wrapper.currency}Rates] (EffectiveDate, Mid, Interpolated)
        VALUES ('{rate.date}', {rate.value}, {rate.interpolated});
        """
        cursor.execute(querry)

def print_rates_table(cursor, currency):
    querry = f"""
    SELECT *
    FROM {currency}Rates;
    """
    cursor.execute(querry)
    for x in cursor.fetchall():
        print(x)

def add_table_currency_mids(wrapper):
    c, conn = connect_to_database()

    create_table(c, wrapper.currency)
    populate_table(c, wrapper)

    conn.commit()
    conn.close()

def summarise_transactions_single_date(currency, date):
    c, conn = connect_to_database()
    pln_wrapper = RatesWrapper("PLN")
    currency_wrapper = RatesWrapper(currency)

    querry_currency = f"""
    SELECT SUBSTR(OrderDate, 0, 11) DATE,
           ROUND(SUM(Quantity * UnitPrice  * (1 - Discount)), 2) TOTAL{currency}
    FROM [Order] JOIN [OrderDetail] ON [Order].id = [OrderDetail].OrderId
                 JOIN [{currency}Rates] ON DATE = [{currency}Rates].EffectiveDate
    WHERE DATE = {date}
    GROUP BY DATE
    ORDER BY DATE;
    """
    c.execute(querry_currency)
    currency_wrapper.append_from_db(c.fetchall())

    querry_pln = f"""
    SELECT SUBSTR(OrderDate, 0, 11) DATE,
           ROUND(SUM(Quantity * UnitPrice  * (1 - Discount) * Mid), 2) TOTALPLN
    FROM [Order] JOIN [OrderDetail] ON [Order].id = [OrderDetail].OrderId
                 JOIN [{currency}Rates] ON DATE = [{currency}Rates].EffectiveDate
    WHERE DATE = {date}
    GROUP BY DATE
    ORDER BY DATE;
    """
    c.execute(querry_pln)
    pln_wrapper.append_from_db(c.fetchall())

    conn.close()
    return [pln_wrapper, currency_wrapper]
