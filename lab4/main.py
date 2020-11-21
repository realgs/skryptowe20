import api


def average_exchange_rates(currency, days):
    rates = api.get_exchange_rates(currency, days)
    for rate in rates:
        print(rate)


def usd_eur_from_last_half_year():
    average_exchange_rates('USD', 183)
    print('\n\n')
    average_exchange_rates('EUR', 183)


if __name__ == '__main__':
    usd_eur_from_last_half_year()
