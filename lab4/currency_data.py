import datetime as dt
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import requests
from spyder.utils.external.github import ApiError
import config

MAX_COUNT = config.NBP_API_REQUEST_MAX_COUNT
TODAY_DATE = dt.datetime.date(dt.datetime.today())


def get_data(address: str) -> requests.Response:
    response = requests.get(address)
    if response.status_code != 200:
        raise ApiError(address, requests.get, response)
    return response


def get_date_days_ago(days: int, until_date=TODAY_DATE):
    return until_date - dt.timedelta(days=days)


def get_data_between_dates(symbol: str, from_date: dt.datetime.date, to_date: dt.datetime.date):
    address = f'http://api.nbp.pl/api/exchangerates/rates/A/{symbol}/{from_date}/{to_date}/'
    return get_data(address)


def get_currency_rates(symbol: str, days: int, until_date=dt.datetime.date(dt.datetime.today())):
    search_count = int(days / MAX_COUNT)
    days_remaining = days % MAX_COUNT
    data = {
        "table": "",
        "currency": "",
        "code": "",
        "rates": []
    }
    from_date = get_date_days_ago(search_count * MAX_COUNT + days_remaining, until_date)
    to_date = get_date_days_ago(search_count * MAX_COUNT, until_date)
    last_data = get_data_between_dates(symbol, from_date, to_date).json()
    data["rates"] = last_data["rates"]
    data["table"] = last_data["table"]
    data["currency"] = last_data["currency"]
    data["code"] = last_data["code"]
    for i in range(search_count, 0, -1):
        from_date = get_date_days_ago(MAX_COUNT * i, until_date)
        to_date = get_date_days_ago(MAX_COUNT * i - MAX_COUNT, until_date)
        data["rates"].extend(
            get_data_between_dates(symbol=symbol, from_date=from_date, to_date=to_date).json()["rates"])

    dates = [data["rates"][i]["effectiveDate"] for i in range(0, len(data["rates"]))]
    currency_rates = [data["rates"][i]["mid"] for i in range(0, len(data["rates"]))]
    return data["code"], dates, currency_rates


def get_rates_plot(draw_dates: list, dates_counter=20, *draw_rates: (list, str)):
    patches = []
    c = 0
    for rates, code in draw_rates:
        print(f'{code} is color: C{c}')
        plt.plot(draw_dates, rates, label=code, color=f'C{c}')
        patch = mpatches.Patch(label=f'{code} to PLN', color=f'C{c}')
        patches.append(patch)
        c = c + 1

    plt.legend(handles=patches)
    shown_values = [draw_dates[i] for i in range(0, len(draw_dates), int(len(draw_dates) / dates_counter))]
    plt.title("Rates of PLN to USD and EUR")
    plt.xlabel("Dates of rating")
    plt.ylabel("Rates of PLN to currency")
    plt.xticks(shown_values, horizontalalignment='center')
    return plt


if __name__ == '__main__':
    count = 180
    USDcode, d, rUSD = get_currency_rates('USD', count)
    EURcode, _, rEUR = get_currency_rates('EUR', count)
    plot = get_rates_plot(d, 5, (rUSD, USDcode), (rEUR, EURcode))
    plot.show()
    plot.savefig('USD_EUR_TO_PLN.svg')
