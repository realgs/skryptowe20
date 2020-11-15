import json
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import requests

RESPONSE_CORRECT_CODE = 200
MAX_DATA_SERIES_SIZE = 255
CCY_DATE_RANGE_ENDPOINT = \
    "http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date}/{end_date}/"


class RequestFailedException(Exception):
    pass


def __get_endpoints(currencies_iso_codes, num_of_days_to_catch_up, end_date):
    endpoints = []
    chunk_start_date = end_date.date() - timedelta(days=num_of_days_to_catch_up - 1)

    days_left = num_of_days_to_catch_up

    while days_left:
        num_of_days_to_get = min(days_left, MAX_DATA_SERIES_SIZE)
        chunk_end_date = chunk_start_date + timedelta(days=num_of_days_to_get - 1)
        days_left -= num_of_days_to_get

        for ccy in currencies_iso_codes:
            endpoints.append(
                CCY_DATE_RANGE_ENDPOINT.format(currency=ccy, start_date=chunk_start_date, end_date=chunk_end_date))

        chunk_start_date = chunk_end_date + timedelta(days=1)

    return endpoints


def _get_response_data(endpoint):
    response = requests.get(endpoint)

    if not response.status_code == RESPONSE_CORRECT_CODE:
        raise RequestFailedException(
            f"Request for {endpoint} failed with {response.status_code}: {response.text}.")

    data = json.loads(response.text)
    return data


def get_currencies_data(currencies_iso_codes, num_of_days_to_catch_up, end_date=datetime.today()) -> pd.DataFrame:
    result_df = pd.DataFrame()

    endpoints = __get_endpoints(currencies_iso_codes, num_of_days_to_catch_up, end_date)

    for endpoint in endpoints:
        response_data = _get_response_data(endpoint)

        data_df = pd.json_normalize(response_data, record_path='rates', meta=['code'])
        result_df = pd.concat([result_df, data_df])

    result_df.reset_index(inplace=True, drop=True)
    result_df = result_df.pivot(index='effectiveDate', columns='code', values='mid')

    return result_df


def draw_chart(data: pd.DataFrame):
    data.plot(title="Currencies average exchange rate", xlabel="Date", ylabel="Average exchange rate")
    plt.legend().set_title("Currency ISO code")
    plt.locator_params(axis="x", nbins=5)
    plt.show()


if __name__ == '__main__':
    currencies_data_df = get_currencies_data(['USD', 'EUR'], 183)
    currencies_data_df.sort_values('effectiveDate', inplace=True)
    draw_chart(currencies_data_df)
