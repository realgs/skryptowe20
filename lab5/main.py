from currency import get_rate_list, get_listing_coursers_between_date
from connectDB import connect, add_table_to_db, fill_table_usd_rate


def generate_sales_information(currency_to_db_name, data_from, data_to):
    cursor = connect()
    # add_table_to_db(cursor)
    listing_between_date = get_listing_coursers_between_date(currency_to_db_name, data_from, data_to)
    currency_to_db_date_list, currency_to_db_rate_list = get_rate_list(listing_between_date)
    fill_table_usd_rate(cursor, currency_to_db_date_list, currency_to_db_rate_list)


def main():
    # import_usd_eur_mid_year()
    generate_sales_information("USD", "2011-10-01", "2014-05-28")


if __name__ == '__main__':
    main()
