import api
import plot

def average_exchange_rates(currency, days):
    rates = api.get_exchange_rates(currency, days)
    for rate in rates:
        print(rate)


def usd_eur_from_last_half_year():
    average_exchange_rates('USD', 183)
    print('\n\n')
    average_exchange_rates('EUR', 183)


def draw(currency1, currency2, days):
    date_list1, rate_list1 = __get_lists(currency1, days)
    date_list2, rate_list2 = __get_lists(currency2, days)
    plot.draw_plot(currency1, date_list1, rate_list1, currency2, date_list2, rate_list2)


def __get_lists(currency, days):
    rates = api.get_exchange_rates(currency, days)
    date_list = []
    rate_list = []
    for rate in rates:
        date_list.append(rate['effectiveDate'])
        rate_list.append(rate['mid'])
    return date_list, rate_list

if __name__ == '__main__':
    draw('USD', 'EUR', 50)
    #usd_eur_from_last_half_year()
    #average_exchange_rates('usd', 367)
