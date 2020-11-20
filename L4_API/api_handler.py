import requests
from datetime import datetime, timedelta
from matplotlib import cycler, ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PLOT_SIZE_X = 10
PLOT_SIZE_Y = 5
PLOT_LEFT_POS = 0.1
PLOT_BOTTOM_POS = 0.2
PLOT_MARGIN = 0.01
PLOT_TICKS_DAY_INTERVAL = 14
PLOT_TICKS_Y_INTERVAL = 0.1
PLOT_TICKS_MINOR_Y_INTERVAL = 0.01
PLOT_GRID_LW = 0.25
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


def plot(currencies, days):
    colors = cycler('color', ['goldenrod', 'lightsteelblue', 'olive', 'cadetblue'])
    plt.rc('axes', prop_cycle=colors)

    fig, ax = plt.subplots(figsize=(PLOT_SIZE_X, PLOT_SIZE_Y))
    plt.subplots_adjust(left=PLOT_LEFT_POS, bottom=PLOT_BOTTOM_POS)
    plt.margins(x=PLOT_MARGIN)

    x_min = '9999-99-99'
    x_max = '0000-00-00'

    for currency in currencies:
        rates, rate_dates = currency_rates_and_dates(currency, days)
        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in rate_dates]
        code = currency

        plt.plot(dates, rates, label=code)

        if rate_dates[0] < x_min:
            x_min = rate_dates[0]
        if rate_dates[-1] > x_max:
            x_max = rate_dates[-1]

    plt.title("Kursy średnie walut {} w dniach od {} do {}".format(
        ', '.join([str(code) for code in currencies]),
        x_min,
        x_max))
    plt.xlabel("data")
    plt.ylabel("kurs średni")

    legend = plt.legend(loc='best')
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('white')
    plt.grid(axis='y', lw=PLOT_GRID_LW)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=PLOT_TICKS_DAY_INTERVAL))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.yaxis.set_major_locator(ticker.MultipleLocator(PLOT_TICKS_Y_INTERVAL))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(PLOT_TICKS_MINOR_Y_INTERVAL))
    fig.autofmt_xdate()

    plt.show()
    if PLOT_SAVE:
        plt.savefig('rates.svg')
