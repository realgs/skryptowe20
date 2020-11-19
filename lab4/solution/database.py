from os.path import isfile
from datetime import date, datetime
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dt

from rates import daily_exchange_rates_for, Currency, DATE_FORMAT


# Dane dla okresu: 2016-01-01 - 2018-01-01
# SQL Server Sample Database Bike Stores przekonwertowane na SQLite

DB_FILE = "./BikeStores.db"
DB_CUSTOM_DATE_FORMAT = "%Y-%m-%d"
DB_READ_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def connect_to_existing_file(file_):
    if not isfile(file_):
        raise FileNotFoundError(f"File {file_} does not exist.")

    return sqlite3.connect(file_)


def create_currency_table(connection, currency, from_date, to_date):
    if from_date > to_date:
        raise ValueError(
            f"from_date '{from_date}' should be before to_date '{to_date}'"
        )

    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pln_rates (
            date TEXT PRIMARY KEY,
            rate REAL NOT NULL
        )
        """
    )

    days_num = (date.today() - from_date).days
    usd = daily_exchange_rates_for(currency, days_num)
    df = pd.DataFrame(usd)
    df.set_index("date", inplace=True)

    new_index = pd.date_range(from_date, to_date)
    df = df.reindex(index=new_index, method="pad")

    # Fill the remaining None values by looking for the first valid value,
    # in case the data starts on a weekend or holiday (the number of days might vary).
    df.fillna(method="backfill", inplace=True)

    df.index = df.index.strftime(DB_CUSTOM_DATE_FORMAT)

    cursor.executemany(
        """
        INSERT INTO pln_rates VALUES (?,?)
        ON CONFLICT(date) DO UPDATE SET rate=excluded.rate
        """,
        df.to_records(),
    )

    connection.commit()


def get_sales_in_two_currencies(connection, from_date, to_date):
    if from_date > to_date:
        raise ValueError(
            f"from_date '{from_date}' should be before to_date '{to_date}'"
        )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT order_date, ROUND(SUM(list_price * (1 - discount) * quantity), 2)
        FROM orders O JOIN order_items OI ON O.order_id = OI.order_id
        GROUP BY order_date
        HAVING order_date BETWEEN ? AND ?
        ORDER BY order_date
        """,
        (
            from_date.strftime(DB_READ_DATE_FORMAT),
            to_date.strftime(DB_READ_DATE_FORMAT),
        ),
    )

    original_sales = [
        (datetime.strptime(date.split(" ")[0], DB_CUSTOM_DATE_FORMAT), total)
        for date, total in cursor
    ]

    rates = cursor.execute(
        """
        SELECT date, rate
        FROM pln_rates
        WHERE date BETWEEN ? AND ?
        ORDER BY date
        """,
        (
            from_date.strftime(DB_CUSTOM_DATE_FORMAT),
            to_date.strftime(DB_CUSTOM_DATE_FORMAT),
        ),
    )

    rates = [
        (datetime.strptime(date, DB_CUSTOM_DATE_FORMAT), rate) for date, rate in cursor
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

    return sales, exchanged_sales


def draw_chart_for(sales, exchanged_sales):
    plt.figure(figsize=(10, 5))
    plt.gca().xaxis.set_major_formatter(dt.DateFormatter(DATE_FORMAT))

    plt.plot(
        exchanged_sales["date"],
        exchanged_sales["total"],
        label="Sales [PLN]",
        linewidth=0.9,
        alpha=0.9,
    )
    plt.plot(
        sales["date"], sales["total"], label="Sales [USD]", linewidth=0.9, alpha=0.9
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
    connection = connect_to_existing_file(DB_FILE)
    from_date = date(2016, 1, 1)
    to_date = date(2018, 1, 1)

    days_num = (date.today() - from_date).days
    create_currency_table(connection, Currency.USD, from_date, to_date)
    sales, exchanged_sales = get_sales_in_two_currencies(connection, from_date, to_date)
    draw_chart_for(sales, exchanged_sales)

    connection.close()
