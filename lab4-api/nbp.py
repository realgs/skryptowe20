#!/bin/python3

import json
import requests
from enum import Enum
from typing import Any, Tuple, List
from datetime import datetime, timedelta

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

    def __init__(self, code: str, table: str) -> None:
        self.code = code
        self.table = table


def request_data(api_url: str) -> Tuple[Any, bool]:
    json_data = Any
    result = False
    try:
        response = requests.get(api_url, params={"?format": "json"})
        if response:
            json_data = response.json()
            result = True
    except requests.RequestException as err:
        print(f"Failed to process request ERROR: {err}")
    except json.JSONDecodeError as err:
        print(f"Failed to decode json ERROR: {err}")
    except Exception as err:
        print(f"unexpected error ERROR: {err}")

    return json_data, result


def rates_time_range(currency: Currency, start_date: datetime, end_date: datetime) -> List[Tuple[float, str]]:
    total_days = (end_date - start_date).days
    if total_days < 0:
        raise ValueError("dates are in wrong order")

    data: List[Tuple[float, str]] = []

    # split ranges into chunks to meet API requirements
    chunks: List[Tuple[str, str]] = []
    while total_days >= 0:
        if total_days == 0:
            chunks.append((start_date.strftime(DATE_FORMAT),
                           start_date.strftime(DATE_FORMAT)))
            break

        days = min(total_days, API_DAYS_LIMIT)
        end_date = start_date + timedelta(days=days)
        chunks.append((start_date.strftime(DATE_FORMAT),
                       end_date.strftime(DATE_FORMAT)))
        total_days -= days + 1
        start_date = end_date + timedelta(days=1)

    for chunk in chunks:
        api_response, request_result = request_data(
            f"{API_URL_RATES}{currency.table}/{currency.code}/{chunk[0]}/{chunk[1]}")

        if request_result:
            for rate in api_response[ApiFields.RATES]:
                data.append(
                    (rate[ApiFields.MID], rate[ApiFields.EFFECTIVE_DATE]))

    return data


def last_rates(currency: Currency, days_back: int = 0) -> List[Tuple[float, str]]:
    '''
    1. Stworzyć funkcję pobierającą średnie kursy notowań zadanej parametrem waluty z ostatnich X dni.
    '''
    if days_back < 0:
        raise ValueError("days count cannot be lower than zero")

    now = datetime.now()
    return rates_time_range(currency, now - timedelta(days=days_back), now)
