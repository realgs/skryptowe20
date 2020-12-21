from currency import get_rate_list, get_listing_coursers_between_date
from connectDB import connect, add_currency_rate_table_to_db, fill_table_currency_rate, add_daily_turnover_table_to_db

MY_DB_DATE_FROM = "2011-10-01"
MY_DB_DATE_TO = "2014-05-28"


def generate_sales_information(currency_to_db_name, data_from, data_to):
    cursor = connect()
    # ### creating DB ### #
    # add_daily_turnover_table_to_db(cursor)
    # add_currency_rate_table_to_db(cursor)
    # ################### #

    # listing_between_date = get_listing_coursers_between_date(currency_to_db_name, data_from, data_to)
    # currency_data = get_rate_list(listing_between_date)
    # fill_table_currency_rate(cursor, currency_data, "PLN")


def main():
    generate_sales_information("USD", MY_DB_DATE_FROM, MY_DB_DATE_TO)


if __name__ == '__main__':
    main()
