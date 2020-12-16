"""
Stores method used to obtain currency data from http://api.nbp.pl/api.
"""
import json
from collections import namedtuple
from datetime import timedelta

import pandas as pd
import requests

from utils import *

API_LIMIT = 367
CCY_DATE_RANGE_ENDPOINT = "http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date}/{end_date}/"


def get_currencies_daily_ex_rates(currencies_iso_codes, start_date, end_date=datetime.today()):
    result_df = pd.DataFrame()
    endpoints = __get_endpoints(currencies_iso_codes, start_date, end_date)

    for endpoint in endpoints:
        response_data = __get_response_data(endpoint)

        data_df = pd.json_normalize(response_data, record_path='rates', meta=['code'])
        result_df = pd.concat([result_df, data_df])

    result_df.reset_index(inplace=True, drop=True)
    result_df = result_df.pivot(index='effectiveDate', columns='code', values='mid')

    return result_df


def __get_endpoints(currencies_iso_codes, start_date, end_date):
    date_chunks = __get_date_chunks(start_date, end_date)
    endpoints = [
        CCY_DATE_RANGE_ENDPOINT.format(currency=ccy, start_date=DateChunk.start_date, end_date=DateChunk.end_date)
        for ccy in currencies_iso_codes
        for DateChunk in date_chunks
    ]

    return endpoints


def __get_date_chunks(start_date, end_date):
    DateChunk = namedtuple('DateChunk', 'start_date end_date')
    date_chunks = []
    days_left = (end_date - start_date).days
    chunk_start_date = start_date

    while days_left > 0:
        chunk_end_date = (chunk_start_date + timedelta(days=min(days_left, API_LIMIT)))
        date_chunks.append(DateChunk(chunk_start_date.date(), chunk_end_date.date()))

        days_left -= (min(days_left, API_LIMIT) + 1)
        chunk_start_date = chunk_end_date + timedelta(days=1)

    return date_chunks


def __get_response_data(endpoint):
    response = requests.get(endpoint)

    data = json.loads(response.text)
    return data


def complete_usd_daily_ex_rates(usd_daily_ex_rates, start_date, end_date):
    usd_daily_ex_rates["interpolated"] = False
    ref_price = usd_daily_ex_rates.loc[usd_daily_ex_rates.index[0]][USD_ISO_CODE]
    for date in ((start_date + timedelta(days=i)) for i in range((end_date - start_date).days)):
        date = date.strftime(DATE_FORMAT)

        if date not in usd_daily_ex_rates.index:
            usd_daily_ex_rates.at[date, USD_ISO_CODE] = ref_price
            usd_daily_ex_rates.at[date, "interpolated"] = True
        else:
            ref_price = usd_daily_ex_rates.loc[date][USD_ISO_CODE]
    usd_daily_ex_rates.sort_index(inplace=True)

    return usd_daily_ex_rates


def get_complete_usd_daily_ex_rates(start_date, end_date):
    usd_daily_ex_rates = get_currencies_daily_ex_rates([USD_ISO_CODE], start_date, end_date)
    return complete_usd_daily_ex_rates(usd_daily_ex_rates, start_date, end_date)
