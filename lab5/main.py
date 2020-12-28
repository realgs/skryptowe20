import currency_api as api
import database as db
import data_file as df


def generate_information(currency, data_from, date_to):
    cursor = db.connect()

    # create
    db.create_currency_table(cursor)
    db.create_daily_sales_table(cursor)

    # insert
    data = api.get_currency_rates_list(api.get_currency_rates_by_dates(currency, data_from, date_to))
    db.fill_currency_table(cursor, data, "PLN")


if __name__ == '__main__':
    generate_information("USD", df.DATABASE_DATE_FROM, df.DATABASE_DATE_TO)
