from datetime import datetime
from datetime import timedelta
import json
import requests


class currency_info:

    COURSE_KEY = 'mid'
    DATE_KET = 'effectiveDate'

    def __init__(self, currency: str, nbp_api_dictionary: dict):
        self.currency = currency
        self.exchange_rate = nbp_api_dictionary[self.COURSE_KEY]
        self.date = datetime.strptime(nbp_api_dictionary[self.DATE_KET], nbp_api.DATE_FORMAT)

    def __str__(self):
        return f'{self.currency}, {self.date.strftime(nbp_api.DATE_FORMAT)}, {self.exchange_rate}'
    
    def __repr__(self):
        return str(self)

    def toJSON(self):
        self_json = self.__dict__
        self_json['date'] = self_json['date'].strftime(nbp_api.DATE_FORMAT)
        return self_json


class nbp_api:

    DATE_FORMAT = '%Y-%m-%d'
    MAX_DAYS_IN_RANGE = 365
    TABLES = ('a', 'b')

    def get_currency_delta(self, currency: str, delta: int, date_to = None):
        if date_to is None:
            date_to = datetime.now()
        delta -= 1
        date_from = date_to - timedelta(days=delta)
        return self.get_currency(currency, date_from, date_to)

    def get_currency(self, currency: str, date_from, date_to):
        if(date_from <= date_to):
            date_ranges = self.date_to_ranges(date_from, date_to)
            responses = []
            for date_range in date_ranges:
                d_from, d_to = date_range
                for table in self.TABLES:
                    url = self.generate_url(table, currency, d_from, d_to)
                    response = requests.get(url)
                    if response.status_code == 200:
                        responses.extend(self.parse_response(currency, response))
            return responses
        return []

    def generate_url(self, table: str, currency: str, date_from: str, date_to: str):
        return f'http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{date_from.strftime(self.DATE_FORMAT)}/{date_to.strftime(self.DATE_FORMAT)}'

    def date_to_ranges(self, date_from, date_to):
        date_ranges = []
        while (date_to - date_from).days > self.MAX_DAYS_IN_RANGE:
            next_item = date_from + timedelta(days=self.MAX_DAYS_IN_RANGE)
            date_ranges.append((date_from, next_item))
            date_from = next_item + timedelta(days=1)
        date_ranges.append((date_from, date_to))
        return date_ranges

    def parse_response(self, currency: str, response):
        response_json = response.json()
        return [ currency_info(currency, response_dict) for response_dict in  response_json['rates']]


if __name__ == '__main__':
    api = nbp_api()
    eur_range = api.get_currency('eur', datetime(2020, 12, 18), datetime(2021, 1, 17))
    print(eur_range)
    eur_delta = api.get_currency_delta('eur', 7300)
    print(eur_delta)
    # usd = api.get_currency_delta('usd', 30)

