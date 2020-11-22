import api
import plot
import database
import total_sales_plot


def average_exchange_rates(currency, days):
    date_list, rate_list = api.get_exchange_rates(currency, days)
    print(f'{currency.upper()} - PLN:')
    print_lists(date_list, rate_list)


def print_lists(list1, list2):
    for i in range(len(list1)):
        print(f'{list1[i]} - {list2[i]}')


def usd_eur_from_last_half_year():
    average_exchange_rates('USD', 183)
    print('\n\n')
    average_exchange_rates('EUR', 183)


def draw(currency1, currency2, days):
    date_list1, rate_list1 = api.get_exchange_rates(currency1, days)
    date_list2, rate_list2 = api.get_exchange_rates(currency2, days)
    plot.draw_plot(currency1, date_list1, rate_list1, currency2, date_list2, rate_list2)


def __get_lists(currency, days):
    rates = api.get_exchange_rates(currency, days)
    date_list = []
    rate_list = []
    for rate in rates:
        date_list.append(rate['effectiveDate'])
        rate_list.append(rate['mid'])
    return date_list, rate_list


def create_table_in_database():
    conn, cursor = database.connect()
    database.create_table(cursor)
    date_list, rate_list = api.get_exchange_rates_date_to_date('usd', '2012-01-01', '2014-06-27')
    database.fill_table(conn, cursor, date_list, rate_list)


def create_total_sales_plot():
    conn, cursor = database.connect()
    data_list = database.get_data_from_database(cursor, '2012-01-01', '2014-06-27')
    total_sales_plot.create_chart_of_total_sales(data_list)


if __name__ == '__main__':
    draw('USD', 'EUR', 50)
    usd_eur_from_last_half_year()
    average_exchange_rates('usd', 500)
    # create_table_in_database() -used once at the beginning
    create_total_sales_plot()
