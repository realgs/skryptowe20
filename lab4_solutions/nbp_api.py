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


def response_handler(response):
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
            result += response_handler(response)

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
    if number_of_last_days < 0:
        raise ArgumentException(
            'Error. Number of last days cannot be negative.')

    current_date = date.today()
    if number_of_last_days == 0:
        return get_avg_rates_from_period(currency, current_date, current_date)

    starting_date = current_date - timedelta(number_of_last_days - 1)
    return get_avg_rates_from_period(currency, starting_date, current_date)


def print_chart_for_two_currencies(first_currency_data, second_currency_data, first_currency, second_currency):
    first_df = pd.DataFrame(data=first_currency_data)
    second_df = pd.DataFrame(data=second_currency_data)

    fig, axs = plt.subplots(figsize=(12, 4))

    axs.plot(first_df['date'], first_df['exchange_rate'], 'b-', label=first_currency.value)
    axs.plot(second_df['date'], second_df['exchange_rate'], 'g-', label=second_currency.value)

    axs.xaxis.set_major_locator(ticker.MaxNLocator(25))
    plt.gcf().autofmt_xdate(rotation=30)
    plt.title('Average exchange rates for {} and {}'.format(first_currency.value, second_currency.value))
    plt.xlabel("Date")
    plt.ylabel("Exchange rate (in terms to PLN)")
    plt.margins(0, None)
    fig.tight_layout()
    plt.legend(loc='right').set_title('Currency')
    plt.savefig("avg_exchange_rates.svg")


if __name__ == '__main__':
    number_of_days_half_year = 365 // 2

    result_eur = get_avg_rates_from_last_x_days(Currency.EUR, number_of_days_half_year)
    result_usd = get_avg_rates_from_last_x_days(Currency.USD, number_of_days_half_year)
    print_chart_for_two_currencies(result_eur, result_usd, Currency.EUR, Currency.USD)
