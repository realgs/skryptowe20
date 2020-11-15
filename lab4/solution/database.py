from os.path import isfile
from datetime import date, timedelta, datetime
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dt

from rates import daily_exchange_rates_for, Currency, DATE_FORMAT


# Pelna wersja AdventureWorks
# Zawiera sprzedaz tylko od 2011 do 2014, robie wykres dla calego tego okresu.
# Srednie notowania dla USD od 2010
AW_DATABSE_FILE = "./AdventureWorks2019.sqlite"
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
    df = df.reindex(index=new_index, method="pad")

    # Fill the remaining None values by looking for the first valid value,
    # in case the data starts on a weekend or holiday (the number of days might vary).
    df.fillna(method="backfill", inplace=True)

    df.index = df.index.strftime(DATABASE_DATE_FORMAT)

    cursor.executemany(
        """
        INSERT INTO pln_rates VALUES (?,?)
        ON CONFLICT(date) DO UPDATE SET rate=excluded.rate
        """,
        df.to_records(),
    )

    connection.commit()


def chart_sales_in_two_currencies(connection, days_num):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT orderdate, SUM(totaldue) FROM salesorderheader
        GROUP BY orderdate
        ORDER BY orderdate
        """
    )

    original_sales = [
        (datetime.strptime(date.split("T")[0], DATABASE_DATE_FORMAT), total)
        for date, total in cursor
    ]

    rates = cursor.execute("SELECT date, rate FROM pln_rates ORDER BY date")
    rates = [
        (datetime.strptime(date, DATABASE_DATE_FORMAT), rate) for date, rate in cursor
    ]

    sales_headers = ["date", "total"]
    sales = pd.DataFrame(original_sales, columns=sales_headers)
    rates = pd.DataFrame(rates, columns=["date", "rate"])

    # Select rates for days present in sales
    rates = rates.loc[rates["date"].isin(sales["date"])].reset_index(drop=True)

    exchanged_total_column = sales["total"].multiply(rates["rate"], axis=0)
    exchanged_sales = pd.concat(
        [sales["date"], exchanged_total_column], axis=1, keys=sales_headers
    )

    plt.gca().xaxis.set_major_formatter(dt.DateFormatter(DATE_FORMAT))

    plt.plot(
        exchanged_sales["date"],
        exchanged_sales["total"],
        label="Sales [PLN]",
        alpha=0.7,
        linewidth=0.8,
    )
    plt.plot(
        sales["date"], sales["total"], label="Sales [USD]", alpha=0.7, linewidth=0.8
    )

    plt.gcf().autofmt_xdate()

    plt.title("Sales in USD and PLN over time")
    plt.xlabel("Date [YYYY-MM-DD]")
    plt.ylabel("Sales")
    plt.tight_layout()

    plt.margins(0, None)
    plt.legend()

    plt.savefig("sales.svg")


if __name__ == "__main__":
    connection = connect_to_existing_file(AW_DATABSE_FILE)

    days_num = (date.today() - date(2010, 1, 1)).days
    create_currency_table(connection, Currency.USD, days_num)
    chart_sales_in_two_currencies(connection, days_num)

    connection.close()
