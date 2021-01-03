from datetime import date, timedelta
import requests

URL = 'http://api.nbp.pl/api/exchangerates/rates/a/'
STATUS_OK = 200


def insert_rates(c_dict, resp):
    for rate in resp.json()['rates']:
        c_dict[rate['effectiveDate']] = {}
        c_dict[rate['effectiveDate']]['rate'] = rate['mid']


def get_currency_rates(start, end, currency):
    start_year = start.year
    end_year = end.year
    rates_dict = {}
    if start_year != end_year:
        resp = requests.get(URL + currency + '/' + start.strftime('%Y-%m-%d') +
                            '/' + str(start_year) + '-12-31/')
        if resp.status_code == STATUS_OK:
            insert_rates(rates_dict, resp)
            start_year = start_year + 1

    while start_year != end_year:
        resp = requests.get(URL + currency + '/' + str(start_year) + '-01-01/' + str(start_year) + '-12-31/')
        if resp.status_code == STATUS_OK:
            insert_rates(rates_dict, resp)
            start_year = start_year + 1

    if start != end:
        resp = requests.get(URL + currency + '/' + str(end_year) + '-01-01/' + end.strftime('%Y-%m-%d') + '/')
    else:
        resp = requests.get(URL + currency + '/' + end.strftime('%Y-%m-%d') + '/')

    if resp.status_code == STATUS_OK:
        insert_rates(rates_dict, resp)

    return rates_dict


def get_daily_currency_rates(start, end, currency):
    start = date.fromisoformat(start)
    end = date.fromisoformat(end)
    delta = end - start
    rates_dict = get_currency_rates(start, end, currency)
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        if day.strftime("%Y-%m-%d") in rates_dict:
            rates_dict[day.strftime("%Y-%m-%d")]['interpolated'] = False
        else:
            rates_dict[day.strftime("%Y-%m-%d")] = {}
            if day != start:
                rates_dict[day.strftime("%Y-%m-%d")]['rate'] = \
                    rates_dict[(day - timedelta(days=1)).strftime("%Y-%m-%d")]['rate']
            else:
                k = 1
                resp = requests.get(URL + currency + '/' + (day - timedelta(days=k)).strftime("%Y-%m-%d") + '/')
                while resp.status_code != STATUS_OK:
                    k = k + 1
                    resp = requests.get(URL + currency + '/' + (day - timedelta(days=k)).strftime("%Y-%m-%d") + '/')
                rates_dict[day.strftime("%Y-%m-%d")]['rate'] = resp.json()['rates'][0]['mid']
            rates_dict[day.strftime("%Y-%m-%d")]['interpolated'] = True
    return rates_dict
