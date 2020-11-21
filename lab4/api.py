import requests as req
from datetime import date
from datetime import timedelta
import datetime as dt

NBP_API_URL = 'http://api.nbp.pl/api/exchangerates/rates/'
MAX_DAYS_AMOUNT = 367


def get_elem(url):
    return req.get(url).json()


def get_exchange_rates(currency, days, days_difference=0):
    date_from = date.today() - timedelta(days=days_difference) - timedelta(days=days)
    if days > MAX_DAYS_AMOUNT:
        date_to = date_from + timedelta(days=MAX_DAYS_AMOUNT)
    else:
        date_to = date.today() - timedelta(days=days_difference)

    all_rates_json = []

    main_date_from = date_from

    while date_to <= date.today() - timedelta(days=days_difference):
        url = f'{NBP_API_URL}/a/{str(currency)}/{str(date_from)}/{str(date_to)}'
        all_rates_json.append(get_elem(url))
        date_from = date_to + timedelta(days=1)
        date_to = date_from + timedelta(days=MAX_DAYS_AMOUNT)

        if date_to > date.today() > date_from:
            date_to = date.today()

    date_list, rate_list = add_weekends(all_rates_json, main_date_from, days)

    return date_list, rate_list


def add_weekends(json_list, date_from, days):
    date_list = []
    rates_list = []
    date_counter = 0
    for json in json_list:
        for elem in json['rates']:
            current_date = dt.datetime.strptime(elem['effectiveDate'], '%Y-%m-%d')

            if len(date_list) == 0:
                date_before = dt.datetime.strptime(str(date_from), '%Y-%m-%d')
                while date_before < current_date:
                    date_list.append(date_before)
                    rates_list.append(elem['mid'])
                    date_before += timedelta(days=1)
                    date_counter += 1
                continue

            next_date = date_list[len(date_list) - 1] + timedelta(days=1)
            while (next_date != current_date) & (not date_counter == days - 1):
                date_list.append(next_date)
                rates_list.append(rates_list[len(rates_list) - 1])
                next_date += timedelta(days=1)
                date_counter += 1

            date_list.append(current_date)
            rates_list.append(elem['mid'])
            date_counter += 1

    return date_list, rates_list


def get_exchange_rates_date_to_date(currency, date_from, date_to):
    date_from = dt.datetime.strptime(str(date_from), '%Y-%m-%d')
    date_to = dt.datetime.strptime(str(date_to), '%Y-%m-%d')
    today = dt.datetime.strptime(str(date.today()), '%Y-%m-%d')
    days = (date_to - date_from).days
    days_difference = (today - date_to).days
    return get_exchange_rates(currency, days, days_difference)
