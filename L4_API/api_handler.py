import requests
from datetime import datetime, timedelta
from matplotlib import cycler
import matplotlib.pyplot as plt

PLOT_TICKS = 10
PLOT_SIZE_X = 10
PLOT_SIZE_Y = 5

PLOT_SAVE = False


def currency_rates_and_dates(currency_code, days):
    date_from = (datetime.today() - timedelta(days=days - 1)).strftime('%Y-%m-%d')
    date_to = datetime.today().strftime('%Y-%m-%d')

    rates, dates = currency_rates_and_dates_time_frame(currency_code, date_from, date_to)

    return rates, dates


def currency_rates_and_dates_time_frame(currency_code, date_from, date_to):
    rates = []
    dates = []

    time_frames = split_time_frame(date_from, date_to)

    for frame in time_frames:
        date_from, date_to = frame
        url = __url("api/exchangerates/rates/{}/{}/{}/{}/".format(
            get_table(currency_code),
            currency_code,
            date_from,
            date_to))

        request = requests.get(url)
        if request.status_code == 200:
            data = request.json()['rates']
            n = len(data)

            for i in range(n):
                rates.append(float(data[i]['mid']))
                dates.append(data[i]['effectiveDate'])

    fill_in_missing_rates(rates, dates)

    return rates, dates


def split_time_frame(date_from, date_to):
    date_frames = []

    date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
    date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
    temp_date_obj = date_from_obj

    while temp_date_obj < date_to_obj:
        if temp_date_obj.weekday() == 5:
            temp_date_obj = temp_date_obj - timedelta(days=1)
        elif temp_date_obj.weekday() == 6:
            temp_date_obj = temp_date_obj - timedelta(days=2)

        new_from = temp_date_obj
        new_to = new_from + timedelta(days=366)

        if new_to > date_to_obj:
            new_to = date_to_obj

        date_frames.append((new_from.strftime('%Y-%m-%d'), new_to.strftime('%Y-%m-%d')))
        temp_date_obj = new_to + timedelta(days=1)

    return date_frames


def fill_in_missing_rates(rates, dates):
    if len(rates) > 1:
        first_day = datetime.strptime(dates[0], '%Y-%m-%d')
        last_day = datetime.strptime(dates[len(dates) - 1], '%Y-%m-%d')

        delta = (last_day - first_day).days

        for i in range(delta):
            date = (first_day + timedelta(days=i)).strftime('%Y-%m-%d')

            if dates[i] != date:
                dates.insert(i, date)
                rates.insert(i, rates[i - 1])

    return rates, dates


def get_table(currency):
    for table in ['A', 'B']:
        if check_table(currency, table):
            return table
    return ''


def check_table(currency, table):
    found = False
    url = __url("api/exchangerates/tables/{}/last/1/".format(table))
    response = requests.get(url).text

    if currency != '' and currency in response:
        found = True

    return found


def __url(path):
    return 'http://api.nbp.pl/' + path


def plot(currencies_data):
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
        if i % PLOT_TICKS != 0:
            tick.set_visible(False)

    plt.show()
    if PLOT_SAVE:
        plt.savefig('zad3.svg')
