from datetime import datetime
from datetime import timedelta
from nbp_api import nbp_api, currency_info
import pandas as pd


class currency_info_inter:

    def __init__(self, currency: str, exchange_rate: float, date: str, interpolated: bool):
        self.currency = currency
        self.exchange_rate = exchange_rate
        self.date = date
        self.interpolated = interpolated

    def __str__(self):
        return f'{self.currency}, {self.date.strftime(nbp_api.DATE_FORMAT)}, {self.exchange_rate}, {self.interpolated}'
    
    def __repr__(self):
        return str(self)

    def toJSON(self):
        self_json = self.__dict__
        self_json['date'] = self_json['date'].strftime(nbp_api.DATE_FORMAT)
        return self_json


class nbp_api_interpolator:

    FIRST_MISSING_DAY_LOOKUP = 7

    def __init__(self):
        self.api= nbp_api()

    def get_currency_between(self, currency: str, date_from: str, date_to: str):
        if date_from <= date_to:
            result = self.api.get_currency(currency, date_from, date_to)
            return self.append_missing_dates(result, currency, date_from, date_to)
        return []

    def get_currency(self, currency: str, delta: int, date_to=None):
        if date_to is None:
            date_to = datetime.now()
        delta -= 1
        date_from = date_to - timedelta(days=delta)
        return self.get_currency_between(currency, date_from, date_to)

    def append_missing_dates(self, api_result: list, currency: str, date_from, date_to):
        result = []
        if not api_result or api_result[0].date != date_from:
            self.try_append_first_missing_date(result, currency, date_from)
        daterange = pd.date_range(date_from, date_to)
        for date_iterator in daterange:
            if api_result and api_result[0].date.date() == date_iterator.date():
                obj = api_result.pop(0)
                result.append(
                    currency_info_inter(obj.currency, obj.exchange_rate, obj.date, False))
            elif result:
                prev = result[-1]
                if prev.date != date_iterator:
                    result.append(
                        currency_info_inter(prev.currency, prev.exchange_rate, date_iterator, True))
        return result
    
    def try_append_first_missing_date(self, result: list, currency: str, date_from: str):
        res = self.api.get_currency_delta(currency, self.FIRST_MISSING_DAY_LOOKUP, date_from)
        if res != []:
            currency_obj = res[-1]
            result.insert(0, currency_info_inter(
                currency_obj.currency, currency_obj.exchange_rate, date_from, True))


if __name__ == '__main__':
    interpolator = nbp_api_interpolator()
    res = interpolator.get_currency_between('eur', datetime(2020, 10, 10), datetime(2020, 10, 20))
    for elem in res:
        print(elem)

    res = interpolator.get_currency('eur', 365 * 19 + 25)
    for elem in res:
        print(elem)
    
