import L4_API.api_handler as api_hdl
import L4_API.db_handler as db_hdl

CURRENCIES = ['USD', 'EUR']
YEAR = 365


def plot_rates(currency_codes, days):
    currencies_data = []

    for currency in currency_codes:
        rates, dates = api_hdl.currency_rates_and_dates(currency, days)
        entry = {'code': currency,
                 'rates': rates,
                 'dates': dates}
        currencies_data.append(entry)

    api_hdl.plot(currencies_data)


def plot_sales():
    pass


def get_rates(currency_code, days):
    rates, _ = api_hdl.currency_rates_and_dates(currency_code, days)
    return rates


def add_rates_to_db(currency_code, date_from, date_to):
    rates, dates = api_hdl.currency_rates_and_dates_time_frame(currency_code, date_from, date_to)

    for i in range(0, len(rates)):
        db_hdl.add_rate_entry(rates[i], dates[i], currency_code)


if __name__ == '__main__':
    # for currency in CURRENCIES:
    #     print(get_rates(currency, YEAR // 2))
    #
    # plot(CURRENCIES, YEAR // 2)

    # add_rates_to_db('USD', '2009-01-01', '2009-12-31')
    # add_rates_to_db('USD', '2010-01-01', '2010-12-31')
    # add_rates_to_db('USD', '2011-01-01', '2011-12-31')
    # add_rates_to_db('USD', '2012-01-01', '2012-12-31')
    # add_rates_to_db('USD', '2013-01-01', '2013-12-31')
    pass
