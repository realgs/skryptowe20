from enum import Enum
from datetime import timedelta
import datetime as dt
import requests

API_URL_RATES = "http://api.nbp.pl/api/exchangerates/rates/a"
API_DAYS_PER_REQUEST_LIMIT = 367
HALF_YEAR_TIME = 183
DATE_FORMAT = "%Y-%m-%d"


class Currency(Enum):
    UNITED_STATES_DOLLAR = 'USD'
    GREAT_BRITAIN_POUND = "GBP"
    SWISS_FRANC = "CHF"
    CANADIAN_DOLLAR = "CAD"
    EUROPEAN_EURO = 'EUR'
    POLISH_ZLOTY = 'PLN'


def partition_days_for_request(start_date, end_date):
    intervals = []
    total_days = (end_date - start_date).days
    while total_days >= 0:
        days = min(total_days, API_DAYS_PER_REQUEST_LIMIT)
        end_date = start_date + dt.timedelta(days=days)
        intervals.append((start_date, end_date))
        total_days -= days + 1
        start_date = end_date + dt.timedelta(days=1)

    return intervals


def fix_data_from_request(data, start_date, end_date, currency):
    i = 1
    fixed = False
    total_days = (end_date - start_date).days
    if not data or data[0][0] != start_date:
        while not fixed:
            api_response = request_data(f"{API_URL_RATES}/{currency}/{start_date - timedelta(days=i)}")
            if api_response:
                data.insert(0, (start_date, (api_response["rates"][0]["mid"]), True))
                fixed = True
            else:
                i += 1
    i = 1
    for x in range(1, total_days + 1):
        if len(data) <= x or data[x][0] != start_date + timedelta(days=i):
            data.insert(i, (data[i - 1][0] + timedelta(days=1), data[i - 1][1], True))
        i += 1


def request_data(api_url):
    response = requests.get(api_url, params={"?format": "json"})
    if response.status_code == 404:
        return None
    if response.status_code != 200:
        raise requests.exceptions.RequestException(
            f"Request for {api_url} returned code {response.status_code}: {response.text}")

    return response.json()


def request_between_dates(currency, start_date, end_date):
    data = []
    intervals = partition_days_for_request(start_date, end_date)
    for interval in intervals:
        api_response = request_data(f"{API_URL_RATES}/{currency}/{interval[0]}/{interval[1]}")
        if api_response:
            for rate in api_response["rates"]:
                data.append(
                    (dt.datetime.strptime(rate["effectiveDate"], DATE_FORMAT).date(), rate["mid"], False))

    fix_data_from_request(data, start_date, end_date, currency)
    return data
