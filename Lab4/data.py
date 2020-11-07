from constants import DEFAULT_TABLE
class Url:
    api_url = "http://api.nbp.pl/api/exchangerates/rates"

    def __init__(self, currency, start_date, end_date, table=DEFAULT_TABLE):
        self.table = table
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

    def get_url(self):
        return self.api_url + (f"/{self.table}/"
                              f"/{self.currency}/"
                              f"/{self.start_date}/"
                              f"/{self.end_date}/")

class Response_A:
    class Rate:
        def __init__(self, rate):
            self.table_number = rate['no']
            self.effective_date = rate['effectiveDate']
            self.mid = rate['mid']

    def __init__(self, request_response):
        res = request_response.json()
        self.table_type = res['table']
        self.currency = res['currency']
        self.currency_code = res['code']
        self.rates = []
        for rate in res['rates']:
            self.rates.append(self.Rate(rate))
