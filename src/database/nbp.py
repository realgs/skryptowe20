import requests
import json
from datetime import datetime, timedelta


LIMIT = 360 #api limit in days


def fetch_avg_currency(table='a', prev_date='2012-01-01', curr_date='2012-01-31', currency='usd'):
    dates = get_dates(prev_date, curr_date)
    result = []
    for pair in list(zip(dates[:-1], dates[1:])):
        req = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{pair[0]}/{pair[1]}")
        if req.status_code == 200:
            res = from_json_to_list(req.json())
            result += res

    return result


def get_dates(start, end):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    days_left = (end - start).days
    date = start
    dates = [start]

    while days_left > 0:
        date += timedelta(days=min(LIMIT, days_left))
        if date not in dates:
            dates.append(date)

        days_left -= (min(LIMIT, days_left) + 1)
    return [x.strftime('%Y-%m-%d') for x in dates]


def fetch_currency_from_two_tables(prev_date='2012-01-01', curr_date='2012-01-31', currency='usd'):
    tab_a = fetch_avg_currency(prev_date=prev_date, curr_date=curr_date, currency=currency)
    tab_b = fetch_avg_currency(table='b', prev_date=prev_date, curr_date=curr_date, currency=currency)

    return list(set(tab_a + tab_b))


def from_json_to_list(json_file):
    if 'rates' in json_file:
        mids = [x['mid'] for x in json_file['rates']]
        dates = [x['effectiveDate'] for x in json_file['rates']]
        interpolated = [False for x in json_file['rates']]
        return list(zip(mids, dates, interpolated))
    else:
        return []
