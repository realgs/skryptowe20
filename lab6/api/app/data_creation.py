from datetime import date, datetime, timedelta

import pandas as pd
import requests


MAX_DAYS = 365
AVG_TABLE_TYPE = "A"
API_DATE_FORMAT = "%Y-%m-%d"
API_URL = "http://api.nbp.pl/api"
API_MIN_DATE = date(2002, 1, 2)
DB_CUSTOM_DATE_FORMAT = "%Y-%m-%d"
DB_READ_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# Testowane juz przy poprzedniej liscie
def get_date_ranges(days_num):
    if days_num <= 0:
        raise ValueError(f"Number of days '{days_num}' cannot be <= 0")

    today = date.today()
    dates = []

    if days_num <= MAX_DAYS:
        start = today - timedelta(days=days_num - 1)
        dates.append((start, today))
    else:
        current_delta = timedelta(days=MAX_DAYS - 1)
        one_delta = timedelta(days=1)

        current_end = today
        while True:
            current_start = current_end - current_delta

            start = current_start
            end = current_end
            dates.append((start, end))

            days_num -= current_delta.days + 1
            if days_num <= 0:
                break

            current_end = current_start - one_delta

            if days_num < MAX_DAYS:
                current_delta = timedelta(days=days_num - 1)

    dates.reverse()
    return dates


def checked_request_json(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(
            "WARNING:",
            f"Status code '{response.status_code}' when connecting to '{url}'",
            f"Reponse text: '{response.text}'",
            sep="\n",
        )
        return {}

    return response.json()


def get_all_available_daily_exchange_rates(currency):
    days_num = (date.today() - API_MIN_DATE).days

    dates = get_date_ranges(days_num)
    dateless_url = f"{API_URL}/exchangerates/rates/{AVG_TABLE_TYPE}/{currency.value}"

    exchange_rates = []

    for date_ in dates:
        start = date_[0].strftime(API_DATE_FORMAT)
        end = date_[1].strftime(API_DATE_FORMAT)

        url = f"{dateless_url}/{start}/{end}"
        response_json = checked_request_json(url)

        if response_json:
            days = response_json["rates"]
            for day in days:
                exchange_rates.append(
                    {
                        "date": datetime.strptime(
                            day["effectiveDate"], API_DATE_FORMAT
                        ).date(),
                        "rate": day["mid"],
                    }
                )

    return exchange_rates


def create_or_update_currency_table(connection, currency):
    from_date = API_MIN_DATE
    to_date = date.today()

    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pln_rates (
            date TEXT PRIMARY KEY,
            rate REAL NOT NULL,
            interpolated BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )

    usd = get_all_available_daily_exchange_rates(currency)
    df = pd.DataFrame(usd).set_index("date")

    new_index = pd.date_range(from_date, to_date)

    # Reindex with method=None and add new column with True wherever there is a NaN
    df = df.reindex(index=new_index, method=None)
    df["interpolated"] = df.apply(lambda x: pd.isnull(x))

    # Fill the None values, first by looking backwards, then by looking forwards
    # in case the data starts on a weekend or holiday (the number of days might vary).
    df = df.fillna(method="pad").fillna(method="backfill")

    df.index = df.index.strftime(DB_CUSTOM_DATE_FORMAT)

    cursor.executemany(
        """
        INSERT INTO pln_rates VALUES (?,?,?)
        ON CONFLICT(date) DO UPDATE SET
        rate=excluded.rate,
        interpolated=excluded.interpolated
        """,
        df.to_records(),
    )

    connection.commit()


def create_or_update_sales_tables(connection):
    from_date = API_MIN_DATE
    to_date = date.today()

    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS total_sales (
            date TEXT PRIMARY KEY,
            original_sales REAL NOT NULL,
            exchanged_sales REAL NOT NULL
        )
        """
    )

    cursor.execute(
        """
        SELECT order_date, ROUND(SUM(list_price * (1 - discount) * quantity), 2)
        FROM orders O JOIN order_items OI ON O.order_id = OI.order_id
        GROUP BY order_date
        ORDER BY order_date
        """
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

    sales_headers = ["date", "original_total"]
    sales = pd.DataFrame(original_sales, columns=sales_headers)
    rates = pd.DataFrame(rates, columns=["date", "rate"])

    # Select rates for days present in sales
    rates = rates.loc[rates["date"].isin(sales["date"])].reset_index(drop=True)

    sales["exchanged_total"] = (
        sales["original_total"].multiply(rates["rate"], axis=0)
    ).round(2)

    sales = sales.set_index("date")
    sales.index = sales.index.strftime(DB_CUSTOM_DATE_FORMAT)

    cursor.executemany(
        """
        INSERT INTO total_sales VALUES (?,?,?)
        ON CONFLICT(date) DO UPDATE SET
        original_sales=excluded.original_sales,
        exchanged_sales=excluded.exchanged_sales
        """,
        sales.to_records(),
    )

    connection.commit()
