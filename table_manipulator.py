import sqlite3
import exchange_rates_acquirer as rates_acquirer
import datetime

CREATE_TABLE_QUERY = "CREATE TABLE ExchangeRate (date text, rate real)"


def get_rows_from_api(currency_code, start_date, end_date):
    api_rates = rates_acquirer.get_exchange_rates_from_api(currency_code, start_date, end_date)
    all_days_rates = rates_acquirer.expand_exchange_rates_to_range(api_rates, currency_code, start_date, end_date)

    return all_days_rates


if __name__ == "__main__":
    connection = sqlite3.connect("Northwind_large.sqlite")
    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE_QUERY)

    rows = get_rows_from_api("usd", datetime.date(2013, 1, 1), datetime.date(2015, 12, 31))

    cursor.close()
    connection.close()
