from datetime import datetime, timedelta, date

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
import database
from matplotlib import ticker

DATE_FORMAT = '%Y-%m-%d'
LINK = "http://api.nbp.pl/api/exchangerates/rates/a"
HALF_YEAR = 183
API_DAYS_LIMIT = 367

US_DOLLAR = 'USD'
EURO = 'EUR'
POLISH_ZLOTY = 'PLN'


def request_url(currency, start_date, end_date=None):
    url = f"{LINK}/{currency}/{date_to_str(start_date)}/{date_to_str(end_date)}"
    resp = requests.get(url)

    if resp.status_code == 404:
        return None
    elif resp.status_code != 200:
        raise requests.exceptions.RequestException(f"{url} returned {resp.status_code} {resp.text}")

    return resp.json()


def divide_periods(start_date, end_date):
    start_date = to_date(start_date)
    end_date = to_date(end_date)

    periods = []
    total_days = (end_date - start_date).days

    while total_days >= 0:
        period_length = min(total_days, API_DAYS_LIMIT)
        end_date = start_date + timedelta(period_length)
        periods.append((start_date, end_date))
        start_date = end_date + timedelta(1)
        total_days -= period_length + 1

    return periods


def repair_data(start_date, end_date, data, currency):
    start_date = to_date(start_date)
    end_date = to_date(end_date)

    i = 1
    repaired = False
    total_days = (end_date - start_date).days

    if not data or data[0][0] != start_date:
        while not repaired:
            resp = request_url(currency, start_date - timedelta(i))
            if resp:
                data.insert(0, (start_date, resp['rates'][0]['mid']))
                repaired = True
            else:
                i += 1

    i = 0
    while len(data) < total_days - 1:
        if data[i][0] + timedelta(1) != data[i + 1][0]:
            data.insert(i + 1, (data[i][0] + timedelta(1), data[i][1]))
        i += 1


def to_date(date):
    if isinstance(date, datetime):
        return date
    else:
        return datetime.strptime(date, DATE_FORMAT)


def date_to_str(date):
    if date is None:
        return ""
    elif isinstance(date, str):
        return date
    else:
        return datetime.strftime(date, DATE_FORMAT)


def get_currency_between_dates(currency, start_date, end_date):
    data = []
    periods = divide_periods(start_date, end_date)

    for period in periods:
        resp = request_url(currency, period[0], period[1])
        if resp:
            for rate in resp['rates']:
                data.append((to_date(rate['effectiveDate']), rate['mid']))

    repair_data(start_date, end_date, data, currency)
    return data


def get_currency_from_last_days(currency, last_days=1):
    if last_days < 1:
        raise Exception("Parameter days must be equal or higher than 1.")
    elif last_days == 1:
        data = []
        resp = request_url(currency, datetime.today())
        data.append((to_date(resp['rates'][0]['effectiveDate']), resp['rates'][0]['mid']))
    else:
        data = get_currency_between_dates(currency, datetime.today() - timedelta(last_days - 1), datetime.today())

    return data


def draw_chart_between_dates(currency_list, start_date, end_date):
    if not isinstance(currency_list, list):
        print('Argument currency_list is not a list')
    else:
        fig, ax = plt.subplots()
        for currency in currency_list:
            data = get_currency_between_dates(currency, start_date, end_date)

            x = []
            y = []
            for date, value in data:
                x.append(date)
                y.append(value)

            ax.plot(x, y, label=currency)

        plt.gca().xaxis.set_major_formatter(pltdates.DateFormatter(DATE_FORMAT))
        plt.gca().xaxis.set_major_locator(pltdates.DayLocator(interval=30))

        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.05))

        ax.xaxis_date()
        fig.autofmt_xdate()
        plt.title("USD and EUR exchange rate")
        plt.xlabel('Date')
        plt.ylabel('Currency value [PLN]')
        plt.legend()
        plt.grid(True)
        plt.savefig('EURandUSD.svg')
        plt.show()


def draw_sales_chart():
    data = database.get_prices_in_year()
    usd_prices, pln_prices, dates = get_usd_pln_prices_lists(data)

    fig, ax = plt.subplots()

    ax.plot(dates, usd_prices, label=US_DOLLAR)
    ax.plot(dates, pln_prices, label=POLISH_ZLOTY)

    plt.gca().xaxis.set_major_formatter(pltdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(pltdates.DayLocator(interval=30))

    plt.gca().set_ylim(ymin=0)
    plt.gca().set_xlim(xmin=dates[0], xmax=dates[-1])

    ax.xaxis_date()
    fig.autofmt_xdate()
    plt.title("Total sales in USD and PLN")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.savefig("USDandPLNsales.svg")
    plt.show()


def get_usd_pln_prices_lists(data):
    pln_prices = []
    usd_prices = []

    dates = []
    for item in data:
        usd_prices.append(item[1])
        pln_prices.append(item[4])
        dates.append(date(*[int(item) for item in item[0].split('-')]))

    return usd_prices, pln_prices, dates


if __name__ == '__main__':
    # zad 2
    get_currency_from_last_days(US_DOLLAR, HALF_YEAR)
    get_currency_from_last_days(EURO, HALF_YEAR)
    # zad 3
    draw_chart_between_dates([US_DOLLAR, EURO], '2019-05-06', '2020-05-06')
    # zad 5
    draw_sales_chart()
