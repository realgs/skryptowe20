from logic.DataAPI.constants import DEFAULT_TABLE, API_URL

class Url:
    def __init__(self, currency, start_date, end_date, table=DEFAULT_TABLE):
        self.table = table
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return API_URL + (f"/{self.table}/"
                          f"/{self.currency}/"
                          f"/{self.start_date}/"
                          f"/{self.end_date}/")

class RatesWrapper:
    class Rate:
        def __init__(self, date, value, interpolated=False):
            self.date = date
            self.value = value
            self.interpolated = interpolated

        def __str__(self):
            return ("{"
                    f"\"date\":\"{self.date}\","
                    f"\"value\":\"{self.value}\","
                    f"\"interpolated\":\"{self.interpolated}\""
                    "}")

    def __init__(self, currency, start_date="", end_date=""):
        self.start_date = start_date
        self.end_date = end_date
        self.currency = currency
        self.rates = []

    def append_from_response(self, response):
        res = response.json()
        for rate in res['rates']:
            self.rates.append(self.Rate(rate['effectiveDate'], rate['mid']))

        self.rates.sort(key=lambda x: x.date)

    def append_from_db(self, db_rates):
        for date, value in db_rates:
            self.rates.append(self.Rate(date, value))

        self.rates.sort(key=lambda x: x.date)

    def append_single_rate(self, date, value, interpolated):
        self.rates.append(self.Rate(date, value, interpolated))
        self.rates.sort(key=lambda x: x.date)

    def __str__(self):
        out = ("{"
               f"\"currency\":\"{self.currency}\","
               f"\"rates\":[")
        for r in self.rates:
            out += f"{r},"
        out = out.rstrip(",")
        out += ("]}")

        return out
