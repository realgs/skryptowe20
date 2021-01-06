import json
from collections import namedtuple
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import requests

RESPONSE_CORRECT_CODE = 200
API_LIMIT = 367
CCY_DATE_RANGE_ENDPOINT = "http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date}/{end_date}/"


class RequestFailedException(Exception):
    pass


def get_currencies_daily_ex_rates_catchup(currencies_iso_codes, num_of_days_to_catch_up, end_date=datetime.today()):
    start_date = __get_catchup_start_date(num_of_days_to_catch_up, end_date)
    return get_currencies_daily_ex_rates(currencies_iso_codes, start_date, end_date)


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


def draw_chart(data: pd.DataFrame):
    data.plot(title="Currencies exchange rate daily", xlabel="Date", ylabel="Exchange rate", rot=30)
    plt.legend().set_title("Currency ISO code")
    plt.gcf().subplots_adjust(bottom=0.2)

    plt.savefig("eur_and_usd_daily_ex_rates.svg")


def __get_catchup_start_date(catchup_num_of_days, end_date=datetime.today()):
    return end_date - timedelta(days=catchup_num_of_days)


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

    if not response.status_code == RESPONSE_CORRECT_CODE:
        raise RequestFailedException(
            f"Request for {endpoint} failed with {response.status_code}: {response.text}.")

    data = json.loads(response.text)
    return data


if __name__ == '__main__':
    currencies_data_df = get_currencies_daily_ex_rates_catchup(['USD', 'EUR'], 183)
    currencies_data_df.sort_values('effectiveDate', inplace=True)
    draw_chart(currencies_data_df)
