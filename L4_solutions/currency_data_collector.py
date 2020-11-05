import json
from datetime import datetime, timedelta
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import requests

RESPONSE_CORRECT_CODE = 200
MAX_DATA_SERIES_SIZE = 255
CCY_AVG_EXCHANGE_RATE_FROM_DATE_RANGE_ENDPOINT = \
    "http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date}/{end_date}/"


class RequestFailed(Exception):
    pass


def __get_endpoints(currencies_iso_codes: List[str], num_of_days_to_catch_up: int, ignore_today: bool = False) -> List[
    str]:
    endpoints = []
    curr_date = datetime.now().date() if not ignore_today else datetime.now().date() - timedelta(days=1)
    start_date = curr_date - timedelta(days=num_of_days_to_catch_up - 1)

    days_left = num_of_days_to_catch_up

    while days_left:
        num_of_days_to_get = min(days_left, MAX_DATA_SERIES_SIZE)
        end_date = start_date + timedelta(days=num_of_days_to_get - 1)
        days_left -= num_of_days_to_get
        for ccy in currencies_iso_codes:
            endpoints.append(
                CCY_AVG_EXCHANGE_RATE_FROM_DATE_RANGE_ENDPOINT.format(currency=ccy, start_date=start_date,
                                                                      end_date=end_date))
        start_date = end_date + timedelta(days=1)

    return endpoints


def get_currencies_avg_exchange_rate(currencies_iso_codes: List[str], num_of_days_to_catch_up: int,
                                     ignore_today: bool = False) -> pd.DataFrame:
    result_df = pd.DataFrame()

    endpoints: List[str] = __get_endpoints(currencies_iso_codes, num_of_days_to_catch_up, ignore_today)
    print(endpoints)
    for endpoint in endpoints:
        response = requests.get(endpoint)

        if not response.status_code == RESPONSE_CORRECT_CODE:
            raise RequestFailed(
                f"Request for {endpoint} failed. There is no data for given time period. "
                f"Try passing ignore_today=True argument if you suspect today's data is not available yet.")

        data = json.loads(response.text)
        data_df = pd.json_normalize(data, 'rates', ['code'])
        result_df = pd.concat([result_df, data_df])

    result_df.reset_index(inplace=True, drop=True)
    result_df = result_df.pivot(index='effectiveDate', columns='code', values='mid')

    return result_df


def draw_chart(data: pd.DataFrame):
    data.plot(title="Currencies average exchange rate", xlabel="Date", ylabel="Average exchange rate")
    plt.legend().set_title("Currency ISO code")
    plt.show()


if __name__ == '__main__':
    my_df = get_currencies_avg_exchange_rate(['USD', 'EUR'], 153)
    my_df.sort_values('effectiveDate', inplace=True)
    draw_chart(my_df)
