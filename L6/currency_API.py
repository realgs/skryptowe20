#!/usr/bin/python3

import requests
import datetime

API_URL = 'http://api.nbp.pl/api/exchangerates/rates/a/'
API_HEADERS = { 'Accept' : 'application/json' }
REQUEST_TIMEOUT = 30
DEFAULT_MAX_HOPS = 7
MAX_REQUEST_PERIOD = 93

# def string_to_datetime(date_string):
#     return datetime.datetime(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10]))
def string_to_datetime(date_string):
    try: date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError: return False
    return date

def get_daily_currency_markings(currency_code, date, max_hops = DEFAULT_MAX_HOPS):
    date_string = date.strftime("%Y-%m-%d")
    response = requests.get(API_URL + currency_code + '/' + date_string, headers = API_HEADERS, timeout = REQUEST_TIMEOUT)

    if response.status_code != 200:
        if response.status_code == 404:
            print('GET', currency_code, 'from', date_string, 'error', response.status_code, '- data from the previous day')
            previous_day = (date - datetime.timedelta(1))

            if max_hops > 0:
                return { date: (get_daily_currency_markings(currency_code, previous_day, max_hops - 1)[previous_day][0], False) }
            else:
                return {date: (-1.0, False)}
        else:
            print('GET', currency_code, 'from', date_string, 'error', response.status_code)
            return {}
    else:
        rate = response.json()['rates'][0]
        return { string_to_datetime(rate['effectiveDate']) : (rate['mid'], True) }

def fill_uneffecive_markings(markings, currency_code, date_from, date_to):
    if markings:
        if date_from not in markings:
            markings.update(get_daily_currency_markings(currency_code, date_from))

        while(date_from < date_to):
            date_from += datetime.timedelta(1)

            if date_from not in markings:
                print("filling marking for ", date_from)
                markings[date_from] = (markings[date_from - datetime.timedelta(1)][0], False)

    return dict(sorted(markings.items()))

def get_currency_markings(currency_code, date_from, date_to):
    markings = {}
    date_from_string = date_from.strftime("%Y-%m-%d")
    date_to_string = date_to.strftime("%Y-%m-%d")

    try:
        response = requests.get(API_URL + currency_code + '/' + date_from_string + '/' + date_to_string, headers = API_HEADERS, timeout = REQUEST_TIMEOUT)

        if response.status_code != 200:
            print('GET', currency_code, 'from', date_from_string, 'to', date_to_string, 'error', response.status_code)
        else:
            for rate in response.json()['rates']:
                markings[string_to_datetime(rate['effectiveDate'])] = (rate['mid'], True)

    except Exception as exception:
        print('something went wrong with the request: ', exception)

    return fill_uneffecive_markings(markings, currency_code, date_from, date_to)

def get_currency_markings_from_date_range(currency_code, date_from, date_to):
    markings = {}
    end_date = date_to
    start_date = date_from
    days = (date_to - date_from).days

    while days > MAX_REQUEST_PERIOD:
        date_from = end_date - datetime.timedelta(days)
        date_to = date_from + datetime.timedelta(MAX_REQUEST_PERIOD - 1)
        print(date_from.strftime("%Y-%m-%d"))
        print(date_to.strftime("%Y-%m-%d"))
        markings.update(get_currency_markings(currency_code, date_from, date_to))
        days -= MAX_REQUEST_PERIOD

    date_from = end_date - datetime.timedelta(days)
    date_to = end_date
    print(date_from.strftime("%Y-%m-%d"))
    print(date_to.strftime("%Y-%m-%d"))
    markings.update(get_currency_markings(currency_code, date_from, date_to))

    return markings

def get_recent_currency_markings(currency_code, days):
    today = string_to_datetime(datetime.datetime.now().strftime("%Y-%m-%d"))
    start_date = (today - datetime.timedelta(days))

    return get_currency_markings_from_date_range(currency_code, start_date, today)


def get_recent_currency_list_markings(currency_list, days):
    markings = []

    for currency_code in currency_list:
        markings.append(get_recent_currency_markings(currency_code, days))

    return markings
