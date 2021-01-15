import datetime as dt

import requests
from spyder.utils.external.github import ApiError

from src import config

MAX_COUNT = config.NBP_API_REQUEST_MAX_COUNT
TODAY_DATE = dt.datetime.date(dt.datetime.today())


def get_data(address: str) -> requests.Response:
    response = requests.get(address)
    if response.status_code != 200:
        raise ApiError(address, requests.get, response)
    return response


def __get_date_days_ago(days: int, until_date=TODAY_DATE):
    return until_date - dt.timedelta(days=days)


def __get_data_between_dates(symbol: str, from_date: dt.datetime.date, to_date: dt.datetime.date):
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
    from_date = __get_date_days_ago(search_count * MAX_COUNT + days_remaining, until_date)
    to_date = __get_date_days_ago(search_count * MAX_COUNT, until_date)
    last_data = __get_data_between_dates(symbol, from_date, to_date).json()
    data["rates"] = last_data["rates"]
    data["table"] = last_data["table"]
    data["currency"] = last_data["currency"]
    data["code"] = last_data["code"]
    for i in range(search_count, 0, -1):
        from_date = __get_date_days_ago(MAX_COUNT * i, until_date)
        to_date = __get_date_days_ago(MAX_COUNT * i - MAX_COUNT, until_date)
        data["rates"].extend(
            __get_data_between_dates(symbol=symbol, from_date=from_date, to_date=to_date).json()["rates"])

    dates = [data["rates"][i]["effectiveDate"] for i in range(0, len(data["rates"]))]
    currency_rates = [data["rates"][i]["mid"] for i in range(0, len(data["rates"]))]
    return data["code"], dates, currency_rates
