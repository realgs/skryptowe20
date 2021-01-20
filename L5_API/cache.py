from datetime import datetime, timedelta
import time

from L5_API.constants import DATE_FORMAT


class RatesCache:
    time_to_refresh = 86400
    rates = {'USD': {}, 'EUR': {}, 'GBP': {}}

    def __init__(self):
        self.start = time.time()

    def is_cached(self, code, date):
        return date in self.rates[code.upper()]

    def is_cached_time_frame(self, code, date_from, date_to):
        date_from_obj = datetime.strptime(date_from, DATE_FORMAT)
        date_to_obj = datetime.strptime(date_to, DATE_FORMAT)
        temp_date_obj = date_from_obj

        while temp_date_obj <= date_to_obj:
            if not self.is_cached(code, temp_date_obj.strftime(DATE_FORMAT)):
                return False
            temp_date_obj += timedelta(days=1)

        return True

    def get_cached(self, code, date_from, date_to):
        data = []
        temp_date_obj = datetime.strptime(date_from, DATE_FORMAT)
        date_to_obj = datetime.strptime(date_to, DATE_FORMAT)

        while temp_date_obj <= date_to_obj:
            date = temp_date_obj.strftime(DATE_FORMAT)
            data.append({"date": date,
                         "rate": self.rates[code.upper()][date][0],
                         "ipd": self.rates[code.upper()][date][1]})
            temp_date_obj += timedelta(days=1)
        print(data)
        return data

    def refresh(self):
        if time.time() - self.start > self.time_to_refresh:
            self.rates = []
            self.start = time.time()

    def cache(self, code, data):
        for d in data:
            date = d['date']
            rate = (d['rate'], d['ipd'])
            self.rates[code.upper()][date] = rate
