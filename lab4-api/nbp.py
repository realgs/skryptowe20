#!/bin/python3

from datetime import timedelta
import json
import requests
import datetime as dt
from enum import Enum
from typing import Any, Optional, Tuple, List

API_URL_RATES = "http://api.nbp.pl/api/exchangerates/rates/"
API_URL_TABLES = "http://api.nbp.pl/api/exchangerates/tables/"
API_DAYS_LIMIT = 90
DATE_FORMAT = "%Y-%m-%d"


class ApiFields:
    TABLE = "table"
    CURRENCY = "currency"
    CODE = "code"
    RATES = "rates"
    NO = "no"
    EFFECTIVE_DATE = "effectiveDate"
    MID = "mid"


class Currency(Enum):
    UNITED_STATES_DOLLAR = ("USD", "A")
    THAI_BAHT = ("THB", "A")
    AUSTRALIAN_DOLLAR = ("AUD", "A")
    HONG_KONG_DOLLAR = ("HKD", "A")
    CANADIAN_DOLLAR = ("CAD", "A")
    NEW_ZEALAND_DOLLAR = ("NZD", "A")
    EUROPEAN_EURO = ("EUR", "A")
    POLISH_ZLOTY = ("PLN", "")

    def __init__(self, code: str, table: str) -> None:
        self.code = code
        self.table = table

    @property
    def title(self) -> str:
        return self.name.title().replace('_', ' ')


def request_data(api_url: str) -> Optional[Any]:
    json_data = None

    response = requests.get(api_url, params={"?format": "json"})
    if response:
        json_data = response.json()

    return json_data


def rates_time_range(currency: Currency, start_date: dt.date, end_date: dt.date,
                     include_unrated_days: bool = False) -> List[Tuple[float, dt.date]]:
    total_days = (end_date - start_date).days
    if total_days < 0:
        raise ValueError("dates are in wrong order")

    data: List[Tuple[float, dt.date]] = []

    # split ranges into chunks to meet API requirements
    chunks: List[Tuple[str, str]] = []
    tmp_start_date = start_date
    tmp_end_date = end_date
    tmp_total_days = total_days
    while tmp_total_days >= 0:
        if tmp_total_days == 0:
            chunks.append((start_date.strftime(DATE_FORMAT),
                           start_date.strftime(DATE_FORMAT)))
            break

        days = min(tmp_total_days, API_DAYS_LIMIT)
        tmp_end_date = tmp_start_date + dt.timedelta(days=days)
        chunks.append((tmp_start_date.strftime(DATE_FORMAT),
                       tmp_end_date.strftime(DATE_FORMAT)))
        tmp_total_days -= days + 1
        tmp_start_date = tmp_end_date + dt.timedelta(days=1)

    for chunk in chunks:
        api_response = request_data(
            f"{API_URL_RATES}{currency.table}/{currency.code}/{chunk[0]}/{chunk[1]}")

        if api_response:
            for rate in api_response[ApiFields.RATES]:
                data.append(
                    (rate[ApiFields.MID], dt.datetime.strptime(rate[ApiFields.EFFECTIVE_DATE], DATE_FORMAT).date()))

    ###### fill gaps in rates ######
    if include_unrated_days:
        tmp_rates: List[Tuple[float, dt.date]] = []
        day_offset = 1
        missing_rates = None
        while not data or (data and data[0][1] > start_date):
            missing_rates = rates_time_range(
                currency, start_date - timedelta(days=day_offset), start_date)
            if missing_rates:
                data = missing_rates + data
            day_offset += 1

        # add trailing rates if missing
        if data[-1][1] < end_date:
            tmp_date = data[-1][1]
            for _ in range((end_date - data[-1][1]).days):
                tmp_date = tmp_date + timedelta(days=1)
                data.append((data[-1][0], tmp_date))

        # add the rest of missing rates
        if (data[-1][1] - data[0][1]).days > len(data):
            for index, rate in enumerate(data[:-1]):
                days_difference = (data[index + 1][1] - rate[1]).days
                if days_difference > 1:
                    tmp_date = rate[1]
                    for _ in range(days_difference - 1):
                        tmp_date = tmp_date + timedelta(days=1)
                        tmp_rates.append((rate[0], tmp_date))
            data.extend(tmp_rates)
            data.sort(key=lambda item: item[1])

        data = data[-(total_days + 1):]

    return data


def last_rates(currency: Currency, days: int = 1,
               include_unrated_days: bool = False) -> List[Tuple[float, dt.date]]:
    '''
    1. Stworzyć funkcję pobierającą średnie kursy notowań zadanej parametrem waluty z ostatnich X dni.
    '''
    if days < 1:
        raise ValueError("day count cannot be lower than one")

    now = dt.datetime.now().date()
    return rates_time_range(currency, now - dt.timedelta(days=days - 1), now, include_unrated_days)


if __name__ == "__main__":
    # tests
    res = last_rates(Currency.EUROPEAN_EURO, 120, include_unrated_days=True)
    print(len(res))
    res = last_rates(Currency.EUROPEAN_EURO, 120, include_unrated_days=False)
    print(len(res))
    print(rates_time_range(Currency.EUROPEAN_EURO, dt.date(2020, 11, 7),
                           dt.date(2020, 11, 8), include_unrated_days=False))
    print(rates_time_range(Currency.EUROPEAN_EURO, dt.date(2020, 11, 7),
                           dt.date(2020, 11, 8), include_unrated_days=True))
