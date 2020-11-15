from os.path import isfile
from datetime import date, timedelta
import sqlite3

import pandas as pd

from rates import daily_exchange_rates_for, Currency


AW_DATABSE_FILE = "./AdventureWorksLT2019.sqlite"
DATABASE_DATE_FORMAT = "%Y-%m-%d"


def connect_to_existing_file(file_):
    if not isfile(file_):
        raise FileNotFoundError(f"File {file_} does not exist.")

    return sqlite3.connect(file_)


def create_currency_table(connection, currency, days_num):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pln_rates (
            date TEXT PRIMARY KEY,
            rate REAL NOT NULL
        )
        """
    )

    usd = daily_exchange_rates_for(currency, days_num)
    df = pd.DataFrame(usd)
    df.set_index("date", inplace=True)

    today = date.today()
    expected_start = today - timedelta(days=days_num - 1)

    new_index = pd.date_range(expected_start, today)
    df = df.reindex(index=new_index, method="nearest")

    df.index = df.index.strftime(DATABASE_DATE_FORMAT)

    cursor.executemany(
        """
        INSERT INTO pln_rates VALUES (?,?)
        ON CONFLICT(date) DO UPDATE SET rate=excluded.rate
        """,
        df.to_records(),
    )

    connection.commit()


if __name__ == "__main__":
    connection = connect_to_existing_file(AW_DATABSE_FILE)
    create_currency_table(connection, Currency.USD, 1000)

    connection.close()
