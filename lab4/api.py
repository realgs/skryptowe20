import requests as req
from datetime import date
from datetime import timedelta
import datetime as dt

NBP_API_URL = 'http://api.nbp.pl/api/exchangerates/rates/'


def datetime_converter(date_str):
    return dt.datetime.strptime(date_str, '%Y-%m-%d')


def get_exchange_rates(currency, days):
    date_from = date.today() - timedelta(days)
    date_to = date.today()
    answer = req.get(f'{NBP_API_URL}/a/{str(currency)}/{str(date_from)}/{str(date_to)}').json()
    rates = answer['rates']
    for rate in rates:
        rate.pop('no')
    return rates
