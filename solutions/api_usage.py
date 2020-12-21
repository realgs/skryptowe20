import requests
import datetime

MAX_DAYS_FOR_QUERY = 93

def _url(path):
    return 'http://api.nbp.pl' + path + '/?format=json'

def get_exchange_rates(code, start_date, end_date):
    return requests.get(_url(f'/api/exchangerates/rates/a/{code}/{start_date}/{end_date}'))

def get_currency_quotes(currency, start_date, end_date):
    rates = {}
    while start_date < end_date:
        query_end_date = min(start_date + datetime.timedelta(MAX_DAYS_FOR_QUERY), end_date)
        data = get_exchange_rates(currency, start_date, query_end_date)
        if data.status_code != 200:
            raise Exception("Couldn't correctly execute request.")
        else:
            for values in data.json()['rates']:
                rates[values['effectiveDate']] = values['mid']
        start_date += datetime.timedelta(MAX_DAYS_FOR_QUERY)
    return rates
