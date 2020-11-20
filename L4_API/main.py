import L4_API.api_handler as api_hdl
import L4_API.db_handler as db_hdl

CURRENCIES = ['USD', 'EUR']
YEAR = 365


def plot(currency_codes, days):
    currencies_data = []

    for currency in currency_codes:
        rates, dates = api_hdl.currency_rates_and_dates(currency, days)
        entry = {'code': currency,
                 'rates': rates,
                 'dates': dates}
        currencies_data.append(entry)

    api_hdl.plot(currencies_data)


def get_rates(currency_code, days):
    rates, _ = api_hdl.currency_rates_and_dates(currency_code, days)
    return rates


def add_rates_to_db(currency_code, date_from, date_to):
    rates, dates = api_hdl.currency_rates_and_dates_time_frame(currency_code, date_from, date_to)

    for r in enumerate(rates):
        db_hdl.add_rate_entry(rates[r], dates[r], currency_code)


if __name__ == '__main__':

    for currency in CURRENCIES:
        print(get_rates(currency, YEAR // 2))

    plot(CURRENCIES, YEAR // 2)
