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

def print_table(cursor, currency):
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
