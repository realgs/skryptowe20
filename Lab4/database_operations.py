import sqlite3
from constants import DATABASE_PATH

def connect_to_database():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn.cursor(), conn

def create_table(cursor, currency):
    querry = f"DROP TABLE IF EXISTS {currency}Rates;"
    cursor.execute(querry)
    querry = f"""
    CREATE TABLE [{currency}Rates] (
        [EffectiveDate] TEXT,
        [Mid] REAL
    );
    """
    cursor.execute(querry)

def populate_table(cursor, currency, rates):
    for rate in rates:
        querry = f"""
        INSERT INTO [{currency}Rates] (EffectiveDate, Mid)
        VALUES ('{rate.effective_date}', {rate.mid});
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

def add_table_currency_mids(result_pair):
    c, conn = connect_to_database()
    currency, rates = result_pair[0], result_pair[1]
    create_table(c, currency)
    populate_table(c, currency, rates)
    conn.commit()
    conn.close()

def summarise_transactions(currency):
    c, conn = connect_to_database()
    querry_currency = f"""
    SELECT SUBSTR(OrderDate, 0, 11) DATE,
           ROUND(SUM(Quantity * UnitPrice  * (1 - Discount)), 2) TOTAL{currency}
    FROM [Order] JOIN [OrderDetail] ON [Order].id = [OrderDetail].OrderId
                 JOIN [{currency}Rates] ON DATE = [{currency}Rates].EffectiveDate
    WHERE DATE BETWEEN '2017-01-01' AND '2020-01-01'
    GROUP BY DATE
    ORDER BY DATE;
    """
    c.execute(querry_currency)
    result_currency = c.fetchall()

    querry_pln = f"""
    SELECT SUBSTR(OrderDate, 0, 11) DATE,
           ROUND(SUM(Quantity * UnitPrice  * (1 - Discount) * Mid), 2) TOTALPLN
    FROM [Order] JOIN [OrderDetail] ON [Order].id = [OrderDetail].OrderId
                 JOIN [{currency}Rates] ON DATE = [{currency}Rates].EffectiveDate
    WHERE DATE BETWEEN '2017-01-01' AND '2020-01-01'
    GROUP BY DATE
    ORDER BY DATE;
    """

    c.execute(querry_pln)
    result_pln = c.fetchall()

    conn.close()
    return [('PLN', result_pln), (currency, result_currency)]
