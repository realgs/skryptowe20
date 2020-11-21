from currency import get_listing_courses, get_rate_list, get_listing_coursers_between_date
from currencyChart import create_chart_of_two_currency
from connectDB import connect, add_col_to_db, fill_col_usd_rate, get_total_sales_to_chart
from totalSalesChart import create_chart_of_total_sales


def import_usd_eur_mid_year():
    currency1_name = "USD"
    currency2_name = "EUR"
    usd_date_list, usd_rate_list = get_rate_list(get_listing_courses(currency1_name, 182))
    print_two_list_together(usd_date_list, usd_rate_list)
    eur_date_list, eur_rate_list = get_rate_list(get_listing_courses(currency2_name, 182))
    print_two_list_together(eur_date_list, eur_rate_list)
    create_chart_of_two_currency(currency1_name, usd_date_list, usd_rate_list, currency2_name, eur_date_list,
                                 eur_rate_list)


def print_two_list_together(list1, list2):
    for i in range(len(list1)):
        print(str(list1[i]) + " - " + str(list2[i]))


def generate_sales_information(currency_to_db_name, data_from, data_to):
    cursor = connect()
    listing_between_date = get_listing_coursers_between_date(currency_to_db_name, data_from, data_to)
    currency_to_db_date_list, currency_to_db_rate_list = get_rate_list(listing_between_date)
    #add_col_to_db(cursor)
    fill_col_usd_rate(cursor, data_from, data_to, currency_to_db_date_list, currency_to_db_rate_list,
                      currency_to_db_name)
    create_chart_of_total_sales(currency_to_db_name, get_total_sales_to_chart(cursor, data_from, data_to))


def main():
    import_usd_eur_mid_year()
    generate_sales_information("USD", "2011-10-01", "2014-05-28")


if __name__ == '__main__':
    main()
