import currency_api as api
import database as db

MY_DB_DATE_FROM = "2011-10-01"
MY_DB_DATE_TO = "2014-05-28"


def generate_information(currency, data_from, date_to):
    cursor = db.connect()

    # create
    db.create_currency_table(cursor)

    # insert
    data = api.get_currency_rates_list(api.get_currency_rates_by_dates(currency, data_from, date_to))
    db.fill_currency_table(cursor, data, "PLN")


if __name__ == '__main__':
    generate_information("USD", MY_DB_DATE_FROM, MY_DB_DATE_TO)
