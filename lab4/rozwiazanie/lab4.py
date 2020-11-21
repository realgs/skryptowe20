import json
from datetime import date
from datetime import datetime
from datetime import timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests

MAX_DAYS_FOR_QUERY = 300


def get_currency_rates_from_x_last_days(currency, number_of_days):
    today_date = date.today()
    date_x_days_ago = today_date - timedelta(days=number_of_days)
    return get_currency_rates_from_date_range(currency, date_x_days_ago, today_date)


def get_currency_rates_from_date_range(currency, start_date, end_date):
    rates = []
    if type(start_date) is not date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if type(end_date) is not date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    left_days_to_fetch = (end_date - start_date).days
    while left_days_to_fetch > 0:
        number_of_days_to_fetch_now = MAX_DAYS_FOR_QUERY if left_days_to_fetch >= MAX_DAYS_FOR_QUERY else left_days_to_fetch
        left_days_to_fetch -= number_of_days_to_fetch_now
        temp_end_date = start_date + timedelta(days=number_of_days_to_fetch_now)
        data = requests.get(r'http://api.nbp.pl/api/exchangerates/rates/a/' + currency + '/' + str(start_date) + '/' + str(temp_end_date) + '/')
        data_len = len(json.loads(data.text)['rates'])
        exchange_rates = [json.loads(data.text)['rates'][i]['mid'] for i in range(data_len)]
        nbp_dates = [json.loads(data.text)['rates'][i]['effectiveDate'] for i in range(data_len)]
        all_dates = [str(start_date + timedelta(days=i)) for i in range(number_of_days_to_fetch_now - 1)]

        # complete empty dates for weekends and breaks
        for i in range(len(all_dates)):
            if i >= len(nbp_dates):
                exchange_rates.insert(i, exchange_rates[i - 1])
                nbp_dates.insert(i, all_dates[i])
            elif all_dates[i] != nbp_dates[i]:
                exchange_rates.insert(i, exchange_rates[i])
                nbp_dates.insert(i, all_dates[i])

        rates += exchange_rates
        start_date = temp_end_date
    return rates


def print_plot_for_dollar_euro_x_days(days):
    dollar = get_currency_rates_from_x_last_days('usd', days)
    euro = get_currency_rates_from_x_last_days('eur', days)
    today_date = date.today()
    x__days_ago_date = today_date - timedelta(days=days)
    dates = mdates.drange(x__days_ago_date, today_date, timedelta(days=1))
    print_plot_for_currencies(dollar, euro, dates)


def print_plot_for_currencies(dollar, euro, dates):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=int(len(dates) / 10)))
    plt.plot(dates, dollar, dates, euro)
    plt.gcf().autofmt_xdate()

    plt.xlabel('czas')
    plt.ylabel('średni kurs notowań [zł]')
    plt.title('Zależność notowań dolara i euro od czasu')
    plt.legend(['USD', 'EUR'], loc='best')
    plt.savefig('dollar_euro_exchange_rates_chart.svg')
    plt.show()


if __name__ == '__main__':
    print_plot_for_dollar_euro_x_days(183)

