import sqlite3
from logic.DataAPI.constants import DATABASE_PATH, START_DATE, END_DATE, SUMMARY_SUPPORTED_CURRENCIES
from logic.DataAPI.web_data import RatesWrapper
from logic.DataAPI.date_parser import is_date_valid
from logic.DataAPI.exceptions import UnsupportedCurrencyException

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

def add_table_rates(wrapper):
    c, conn = connect_to_database()

    create_table(c, wrapper.currency)
    populate_table(c, wrapper)

    conn.commit()
    conn.close()

def summarise_transactions(currency, start_date, end_date):
    c, conn = connect_to_database()

    querry = f"""
    SELECT SUBSTR(OrderDate, 0, 11) DATE,
           ROUND(SUM(Quantity * UnitPrice  * (1 - Discount)), 2) TOTALORIGINAL,
           ROUND(SUM(Quantity * UnitPrice  * (1 - Discount) / Mid), 2) TOTAL{currency}
    FROM [Order] JOIN [OrderDetail] ON [Order].id = [OrderDetail].OrderId
                 JOIN [{currency}Rates] ON DATE = [{currency}Rates].EffectiveDate
    WHERE DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DATE
    ORDER BY DATE;
    """
    c.execute(querry)
    output = c.fetchall()
    conn.close()
    return output

def create_summary_table(cursor, currency):
    querry = f"DROP TABLE IF EXISTS {currency}Summary;"
    cursor.execute(querry)
    querry = f"""
    CREATE TABLE [{currency}Summary] (
        [Date] TEXT,
        [OriginalSum] REAL,
        [CurrencySum] REAL
    );
    """
    cursor.execute(querry)

def populate_summary_table(cursor, currency, summary):
    for date, original_sum, currency_sum in summary:
        querry = f"""
        INSERT INTO [{currency}Summary] (Date, OriginalSum, CurrencySum)
        VALUES ('{date}', {original_sum}, {currency_sum});
        """
        cursor.execute(querry)

def summary_to_json(summary):
    date, original, currency = summary[0]
    return ("{"
            f"\"date\":\"{date}\","
            f"\"original_sum\":\"{original}\","
            f"\"currency_sum\":\"{currency}\""
            "}")

def validate_currency(currency):
    if not currency in SUMMARY_SUPPORTED_CURRENCIES:
        raise UnsupportedCurrencyException

def get_summary(currency, date):
    validate_currency(currency)
    is_date_valid(date)

    c, conn = connect_to_database()
    querry = f"""
    SELECT *
    FROM [{currency}Summary]
    WHERE Date = '{date}';
    """
    c.execute(querry)
    output = c.fetchall()

    conn.close()
    return output

def add_table_summary(wrapper):
    c, conn = connect_to_database()

    create_summary_table(c, wrapper.currency)
    summary = summarise_transactions(wrapper.currency, START_DATE, END_DATE)
    populate_summary_table(c, wrapper.currency, summary)

    conn.commit()
    conn.close()

def init_database(list_of_wrappers):
    for wrapper in list_of_wrappers:
        add_table_rates(wrapper)
        add_table_summary(wrapper)
