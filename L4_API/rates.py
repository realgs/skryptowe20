import requests
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


def currency_rates(currency_code, days):
    rates = []
    dates = []

    url = _url("api/exchangerates/rates/{}/{}/{}/{}/".format(
        _get_table(currency_code),
        currency_code,
        (datetime.today() - timedelta(days=days - 1)).strftime('%Y-%m-%d'),
        datetime.today().strftime('%Y-%m-%d')))

    request = requests.get(url)
    if request.status_code == 200:
        data = request.json()['rates']
        n = len(data)

        for i in range(n):
            rates.append(float(data[i]['mid']))
            dates.append(data[i]['effectiveDate'])

    return rates, dates


def _get_table(currency):
    for table in ['A', 'B']:
        if _check_table(currency, table):
            return table
    return ''


def _check_table(currency, table):
    found = False
    url = _url("api/exchangerates/tables/{}/last/1/".format(table))
    response = requests.get(url).text

    if currency in response:
        found = True

    return found


def _url(path):
    return 'http://api.nbp.pl/' + path


def plot():

    pass


if __name__ == '__main__':
    days = 182
    rates_usd, dates_usd = currency_rates('USD', days)
    rates_eur, dates_eur = currency_rates('EUR', days)

    print(rates_usd)

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
    plt.yticks(np.arange(round(y_min, 1), round(y_max, 1), 0.1))

    plt.xticks(range(1, len(dates_usd), 10), dates_usd[::10])
    plt.xticks(rotation=90)

    plt.show()
