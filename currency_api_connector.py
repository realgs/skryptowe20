import json
from datetime import date, timedelta

import dateutil.parser
import requests


def get_url_data(url):
    try:
        request = requests.get(url)
        json_data = json.loads(request.text)
        return json_data
    except requests.exceptions.ConnectionError:
        print('No connection')
    except json.decoder.JSONDecodeError as err:
        print('Error occurred while decoding JSON: ', err.doc)
    return None


class CurrencyDataDownloader:
    def __init__(self):
        self.__base_link = 'http://api.nbp.pl/api/'

    def __get_currency_rates_json_data(self, currency, how_many_days):
        max_days_amount = 367
        date_from = date.today() - timedelta(days=how_many_days)
        date_to = date_from + timedelta(days=max_days_amount)
        if date_to > date.today():
            date_to = date.today()
        json_multiple_data = []
        last_date = False
        while date_to <= date.today():
            link_to_data = self.__base_link + f'/exchangerates/rates/a/' \
                                              f'{str(currency).lower()}/{str(date_from)}/{str(date_to)}/'
            json_multiple_data.append(get_url_data(link_to_data))
            date_from = date_to + timedelta(days=1)
            date_to = date_from + timedelta(days=max_days_amount)
            if date_to > date.today() > date_from and not last_date:
                date_to = date.today()
                last_date = True
        currency_code = ''
        if len(json_multiple_data) > 0 and json_multiple_data[0] is not None:
            currency_code = json_multiple_data[0]['code']

        return json_multiple_data, currency_code

    def get_currency_prices_for_last_days(self, currency, how_many_days):
        json_data = self.__get_currency_rates_json_data(currency, how_many_days)
        prices_with_dates = []
        if json_data[0] is not None:
            for data in json_data[0]:
                for rate in data['rates']:
                    prices_with_dates.append((rate['effectiveDate'], rate['mid']))
        return prices_with_dates, json_data[1]

    def get_currency_prices_for_last_half_year(self, currency):
        date_six_months_ago = date.today() - dateutil.relativedelta.relativedelta(months=6)
        delta = date.today() - date_six_months_ago
        return self.get_currency_prices_for_last_days(currency, delta.days)
