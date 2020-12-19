import json
from datetime import date, timedelta
import requests
import matplotlib.pyplot as plt
from exceptions import RequestException, ArgumentException
import matplotlib.ticker as ticker
from currency import Currency
import pandas as pd

NBP_EXCHANGE_RATES_URL = 'http://api.nbp.pl/api/exchangerates/rates/{table_type}/{currency}/{start_date}/{end_date}/'

MAX_DAYS_TO_GET = 367
TABLE_TYPE = 'a'
DATE_FORMAT = "%Y-%m-%d"
SUCCESS_CODE = 200

RATES_KEY = 'rates'
DATE_KEY = 'effectiveDate'
AVG_RATE_KEY = 'mid'


def __response_handler(response):
    if response.status_code != SUCCESS_CODE:
        raise RequestException(
            'Error. Cannot get data from: {}. \n Status code: {}. \n Description: {}'.format(response.url,
                                                                                             response.status_code,
                                                                                             response.text))
    exchange_rates_period = []
    exchange_rates = response.json()[RATES_KEY]
    for day in exchange_rates:
        exchange_rates_period.append({
            "date": day[DATE_KEY],
            "exchange_rate": day[AVG_RATE_KEY]
        })
    return exchange_rates_period


def __exchange_rates_url(table_type, currency, start_date, end_date):
    return NBP_EXCHANGE_RATES_URL.format(table_type=table_type, currency=currency.value, start_date=start_date,
                                         end_date=end_date)


def __send_get_request(currency, start, end):
    response = requests.get(__exchange_rates_url(TABLE_TYPE, currency, start, end))
    return response


def get_avg_rates_from_period(currency, starting_day, ending_day):
    date_diff = (ending_day - starting_day).days
    if date_diff < 0:
        raise ArgumentException(
            'Error. Start date cannot be after the end date.')
    dates = []
    dates.append(ending_day)
    last_ending_day = ending_day

    while (date_diff > MAX_DAYS_TO_GET):
        intermediate_date = last_ending_day - timedelta(MAX_DAYS_TO_GET)
        date_diff -= MAX_DAYS_TO_GET
        dates.append(intermediate_date)
        last_ending_day = intermediate_date

    dates.append(starting_day)
    dates.reverse()
    result = []

    for x in range(len(dates)):
        if (x + 1) != len(dates):
            response = __send_get_request(currency, dates[x], dates[x + 1])
            result += __response_handler(response)

    return __remove_duplicates(result)


def __remove_duplicates(result):
    copy_result = []
    duplicates_indexes = []

    for item in result:
        copy_result.append(json.dumps(item, sort_keys=True))

    for index in range(len(copy_result)):
        if (index + 1) != len(copy_result):
            if copy_result[index] == copy_result[index + 1]:
                duplicates_indexes.append(index)

    distinct_result = []
    for index in range(len(result)):
        if index not in duplicates_indexes:
            distinct_result.append(result[index])

    return distinct_result


def get_avg_rates_from_last_x_days(currency, number_of_last_days):
    if number_of_last_days <= 0:
        raise ArgumentException(
            'Error. Number of last days cannot be negative or 0.')

    current_date = date.today()
    starting_date = current_date - timedelta(number_of_last_days - 1)
    return get_avg_rates_from_period(currency, starting_date, current_date)
