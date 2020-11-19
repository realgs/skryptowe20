import requests
from datetime import datetime, timedelta
from matplotlib import cycler
import matplotlib.pyplot as plt

CURRENCIES = ['USD', 'EUR']
YEAR = 365
TICKS = 10
PLOT_SIZE_X = 10
PLOT_SIZE_Y = 5


def currency_rates_dates(currency_code, days):
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


def _plot(currencies_data):
    colors = cycler('color', ['goldenrod', 'lightsteelblue', 'olive', 'cadetblue'])
    plt.rc('axes', prop_cycle=colors)

    plt.figure(figsize=(PLOT_SIZE_X, PLOT_SIZE_Y))
    plt.subplots_adjust(left=0.1, bottom=0.2)

    x_min = '9999-99-99'
    x_max = '0000-00-00'

    currency_codes = []
    for currency in currencies_data:
        dates = currency['dates']
        rates = currency['rates']
        code = currency['code']

        plt.plot(dates, rates, label=code)

        currency_codes.append(code)
        if dates[0] < x_min:
            x_min = dates[0]
        if dates[-1] > x_max:
            x_max = dates[-1]

    plt.title("Kursy średnie walut {} w dniach od {} do {}".format(
        ', '.join([str(code) for code in currency_codes]),
        x_min,
        x_max))
    plt.xlabel("data")
    plt.ylabel("kurs średni")

    plt.legend(frameon=False, loc='best')
    plt.grid(axis='y', lw=0.25)

    plt.xlim(x_min, x_max)
    _, ticks = plt.xticks()
    for i, tick in enumerate(ticks, start=2):
        tick.set_fontsize(8)
        tick.set_rotation(45)
        if i % TICKS != 0:
            tick.set_visible(False)

    plt.show()


def plot(currency_codes, days):
    currencies_data = []

    for currency in currency_codes:
        rates, dates = currency_rates_dates(currency, days)
        entry = {'code': currency,
                 'rates': rates,
                 'dates': dates}
        currencies_data.append(entry)

    _plot(currencies_data)


if __name__ == '__main__':
    print(currency_rates_dates('USD', YEAR // 2)[0])
    print(currency_rates_dates('EUR', YEAR // 2)[0])
    plot(CURRENCIES, YEAR // 2)
