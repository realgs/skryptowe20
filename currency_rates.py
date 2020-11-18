from datetime import datetime
from datetime import timedelta
import requests
import json

_MAX_DAYS_IN_RANGE = 365

def _get_url(table, currency, prev_date, today):
    return f'http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{prev_date}/{today}'

def _get_date_ranges(delta):
    today = datetime.date(datetime.now())
    previous_date = today - timedelta(days=delta)
    date_ranges = []

    while (today - previous_date).days > _MAX_DAYS_IN_RANGE:
        prev = previous_date
        next = previous_date + timedelta(days=_MAX_DAYS_IN_RANGE)
        date_ranges.append((prev, next))
        previous_date = next + timedelta(days=1)

    date_ranges.append((previous_date, today))

    return date_ranges

def get_rete_of_currency(currency, delta):
    if not isinstance(currency, str) or not isinstance(delta, int):
        raise TypeError('At least one parameter had wrong type')

    if delta <= 0:
        raise ValueError('Delta must be posivite')

    date_ranges = _get_date_ranges(delta)
    results = []

    for date_range in date_ranges:
        url_table_a = _get_url('a', currency, date_range[0], date_range[1])
        url_table_b = _get_url('b', currency, date_range[0], date_range[1])

        ra = requests.get(url_table_a)
        rb = requests.get(url_table_b)

        if ra.status_code == 200:
            results.append(json.loads(ra.text))
        elif rb.status_code == 200:
            results.append(json.loads(rb.text))

    for i in range(1, len(results)):
        results[0]['rates'] = results[0]['rates'] + results[i]['rates']

    if len(results):
        return results[0]
    else:
        return results

if __name__ == '__main__':
    print(json.dumps(get_rete_of_currency('eur', 365 // 2), indent=4))
    print(json.dumps(get_rete_of_currency('usd', 365 // 2), indent=4))
