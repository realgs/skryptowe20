import json
from datetime import date
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import requests
from matplotlib.dates import DayLocator, DateFormatter, drange

MAX_DAYS_FOR_QUERY = 300


def get_currency_rates_from_x_last_days(currency, number_of_days):
    today_date = date.today()
    date_x_days_ago = today_date - timedelta(days=number_of_days - 1)
    return get_currency_rates_from_date_range(currency, date_x_days_ago, today_date)


def get_currency_rates_from_date_range(currency, start_date, end_date):
    rates = [[], [], []]

    if type(start_date) is not date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if type(end_date) is not date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    left_days_to_fetch = (end_date - start_date).days + 1
    interpolated = []

    # check if first day occurs in nbp api, if not then get last valid value
    first_value_interpolated = False
    value_first_day = requests.get(r'http://api.nbp.pl/api/exchangerates/rates/a/' + currency + '/' + str(start_date) + '/')
    if value_first_day.status_code == 404:
        temp_date = start_date - timedelta(days=1)
        while value_first_day.status_code == 404:
            value_first_day = requests.get(r'http://api.nbp.pl/api/exchangerates/rates/a/' + currency + '/' + str(temp_date) + '/')
        value_first_day = json.loads(value_first_day.text)['rates'][0]['mid']
        first_value_interpolated = True

    while left_days_to_fetch > 0:
        number_of_days_to_fetch_now = MAX_DAYS_FOR_QUERY if left_days_to_fetch >= MAX_DAYS_FOR_QUERY else left_days_to_fetch
        left_days_to_fetch -= number_of_days_to_fetch_now
        temp_end_date = start_date + timedelta(days=number_of_days_to_fetch_now - 1)
        data = requests.get(r'http://api.nbp.pl/api/exchangerates/rates/a/' + currency + '/' + str(start_date) + '/' + str(temp_end_date) + '/')
        data_len = len(json.loads(data.text)['rates'])
        exchange_rates = [json.loads(data.text)['rates'][i]['mid'] for i in range(data_len)]
        nbp_dates = [json.loads(data.text)['rates'][i]['effectiveDate'] for i in range(data_len)]
        all_dates = [str(start_date + timedelta(days=i)) for i in range(number_of_days_to_fetch_now)]

        # complete empty dates for weekends and breaks
        for i in range(len(all_dates)):
            if i == 0 and first_value_interpolated is True:
                exchange_rates.insert(0, value_first_day)
                nbp_dates.insert(0, all_dates[0])
                interpolated.insert(0, True)
                first_value_interpolated = False
            elif i >= len(nbp_dates) or all_dates[i] != nbp_dates[i]:
                exchange_rates.insert(i, exchange_rates[i - 1])
                nbp_dates.insert(i, all_dates[i])
                interpolated.insert(i, True)
            else:
                interpolated.insert(i, False)

        rates[0] += exchange_rates
        rates[1] += nbp_dates
        rates[2] += interpolated
        start_date = temp_end_date + timedelta(days=1)
        interpolated = []

    return rates


def print_plot_for_dollar_euro_x_days(days):
    dollar = get_currency_rates_from_x_last_days('usd', days)
    euro = get_currency_rates_from_x_last_days('eur', days)
    # for example dollar[0] has rates, dollar[1] has dates
    if len(dollar[0]) > 0:
        x__days_ago_date = (datetime.strptime(dollar[1][0], "%Y-%m-%d")).date()
        today_date = (datetime.strptime(euro[1][len(euro[1]) - 1], "%Y-%m-%d") + timedelta(days=1)).date()
        dates = drange(x__days_ago_date, today_date, timedelta(days=1))
        print_plot_for_currencies(dollar[0], euro[0], dates)


def print_plot_for_currencies(dollar, euro, dates):
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ratio = int(len(dates) / 10)
    interval = ratio if ratio > 0 else 1
    plt.gca().xaxis.set_major_locator(DayLocator(interval=interval))
    plt.plot(dates, dollar, dates, euro)
    plt.gcf().autofmt_xdate()

    plt.xlabel('czas')
    plt.ylabel('średni kurs notowań [zł]')
    plt.title('Zależność notowań dolara i euro od czasu')
    plt.legend(['USD', 'EUR'], loc='best')
    plt.savefig('dollar_euro_exchange_rates_chart.svg')
    plt.show()

