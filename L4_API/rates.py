import requests
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


def currency_rates(currency_code, days):
    rates = []
    dates = []
    table = get_table(currency_code)

    url = "http://api.nbp.pl/api/exchangerates/rates/" + table + "/" + currency_code \
          + "/" + (datetime.today() - timedelta(days=days-1)).strftime('%Y-%m-%d') \
          + "/" + datetime.today().strftime('%Y-%m-%d') + "/"
    request = requests.get(url)

    if request.status_code == 200:
        request = request.json()['rates']
        n = len(request)
    else:
        return rates, dates

    for i in range(n):
        rates.append(float(request[i]['mid']))
        dates.append(request[i]['effectiveDate'])

    return rates, dates


def get_table(currency):
    for table in ['A', 'B']:
        if check_table(currency, table):
            return table
    return ''


def check_table(currency, table):
    found = False
    url = "http://api.nbp.pl/api/exchangerates/tables/" + table + "/last/1/"
    response = requests.get(url).text

    if currency in response:
        found = True

    return found


if __name__ == '__main__':
    days = 182
    rates_usd, dates_usd = currency_rates('USD', days)
    rates_eur, dates_eur = currency_rates('EUR', days)

    f = plt.figure(figsize=(10, 5))

    x_min = dates_usd[0]
    x_max = dates_usd[len(dates_usd) - 1]
    y_min = min(rates_eur + rates_usd) - 0.1
    y_max = max(rates_eur + rates_usd) + 0.1

    plt.plot(dates_usd, rates_usd, color='goldenrod', label='USD')
    plt.plot(dates_eur, rates_eur, color='lightsteelblue', label='EUR')

    plt.title("Kursy średnie walut EUR i USD w dniach od " + x_min + " do " + x_max)
    plt.xlabel("data")
    plt.ylabel("kurs średni")
    plt.legend(frameon=False, loc='lower left')
    plt.xlim(x_min, x_max)
    plt.grid(axis='y', lw=0.25)

    #
    # plt.locator_params(axis='x', nbins=10)

    plt.yticks(np.arange(round(y_min, 1), round(y_max, 1), 0.1))
    nth = 10
    _, ticks = plt.xticks()
    for i, tick in enumerate(ticks, start=2):
        tick.set_fontsize(9)
        tick.set_rotation('vertical')
        tick.set_visible(False)
        if i % nth == 0:
            tick.set_visible(True)

    plt.show()
    plt.savefig('zad3.svg')
