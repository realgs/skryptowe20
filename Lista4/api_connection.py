import requests
import datetime


def get_average_currency_rates_between(currency, first_day, last_day):
    url = 'http://api.nbp.pl/api/exchangerates/rates/A/' + currency + '/'
    result = []
    end_date = last_day
    days = (last_day - first_day).days
    while days > 0:
        begin_date = end_date - datetime.timedelta(days=min(days, 92))
        response = requests.get(url + begin_date.strftime('%Y-%m-%d') + '/' + end_date.strftime('%Y-%m-%d'))
        if response.status_code == 200:
            result = response.json()['rates'] + result
        days -= 93
        end_date = end_date - datetime.timedelta(days=93)
    return result
