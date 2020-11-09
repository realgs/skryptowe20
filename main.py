import requests
import datetime

currencies_symbols = [
    'usd',
    'pln',
    'chf',
    'eur',
    'gbp'
]


def get_avg_rate(currency, number_of_days):
    current_date = datetime.date.today()
    prev_date = current_date - datetime.timedelta(number_of_days)
    currency_symbol = currency.lower()

    if currency_symbol in currencies_symbols:
        resp = requests.get(
            f'http://api.nbp.pl/api/exchangerates/rates/a/{currency_symbol}/{prev_date}/{current_date}/')
        if resp.status_code != 200:
            print(f'Request error: {resp.status_code}')
            return resp.status_code
        else:
            return resp
    else:
        print(f'Could not get data for currency: {currency_symbol}. Wrong currency symbol')
