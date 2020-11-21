import L4_API.api_handler as api_hdl
import L4_API.db_handler as db_hdl

CURRENCIES = ['USD', 'EUR']
YEAR = 365


def plot_rates(currency_codes, days):
    api_hdl.plot(currency_codes, days)


def plot_sales(currency_code, date_from, date_to):
    db_hdl.plot_sale_time_frame(currency_code, date_from, date_to)


def get_rates(currency_code, days):
    rates, _ = api_hdl.currency_rates_and_dates(currency_code, days)
    return rates


def add_rates_to_db(currency_code, date_from, date_to):
    rates, dates = api_hdl.currency_rates_and_dates_time_frame(currency_code, date_from, date_to)
    db_hdl.add_rate_entries(dates, rates, currency_code)


if __name__ == '__main__':
    for currency in CURRENCIES:
        print(get_rates(currency, YEAR // 2))

    plot_rates(CURRENCIES, YEAR // 2)

    # add_rates_to_db(CURRENCIES[0], '2009-01-02', '2014-12-31')

    plot_sales(CURRENCIES[0], '2010-01-01', '2010-12-31')
