from datetime import datetime
from datetime import timedelta
import requests
import json
from keys import *

__MAX_DAYS_IN_RANGE = 365

def __generate_url(table, currency, prev_date, today):
    return f'http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{prev_date}/{today}'

def __delta_to_ranges(delta):
    today = datetime.date(datetime.now())
    previous_date = today - timedelta(days=delta)
    date_ranges = []

    while (today - previous_date).days > __MAX_DAYS_IN_RANGE:
        prev = previous_date
        next_item = previous_date + timedelta(days=__MAX_DAYS_IN_RANGE)
        date_ranges.append((prev, next_item))
        previous_date = next_item + timedelta(days=1)

    date_ranges.append((previous_date, today))
    return date_ranges

def __convert_array_of_responses(responses):
    rates = []
    for response in responses:
        rates.extend(response[NBP_RATES_OBJECT_KEY])
    
    return list(map(lambda elem: {
            DATE_KEY: datetime.strptime(elem[NBP_DATE_KEY], NBP_DATE_FORMAT),
            RATE_KEY: elem[NBP_RATE_KEY],
            INTERPOLATED_KEY: False
        }, rates))

def __append_missing_dates(rates):
    i = 0
    while i < len(rates) - 1:
        current = rates[i]
        next_item = rates[i + 1]

        delta = next_item[DATE_KEY] - current[DATE_KEY]

        if delta.days > 1:
            rates.insert(i + 1, {
                DATE_KEY: current[DATE_KEY] + timedelta(days=1),
                RATE_KEY: current[RATE_KEY],
                INTERPOLATED_KEY: True
            })

        i += 1
    return rates

def __convert_dates_to_string(rates):
    converted = []
    for rate in rates:
        converted.append({
            DATE_KEY: rate[DATE_KEY].strftime(DATE_FORMAT),
            RATE_KEY: rate[RATE_KEY],
            INTERPOLATED_KEY: rate['interpolated']
        })
    return converted

def get_rete_of_currency(currency, delta):
    if not isinstance(currency, str) or not isinstance(delta, int):
        raise TypeError('At least one parameter had wrong type')

    if delta <= 0:
        raise ValueError('Delta must be posivite')

    date_ranges = __delta_to_ranges(delta)
    responses = []

    for date_range in date_ranges:
        url_table_a = __generate_url('a', currency, date_range[0], date_range[1])
        url_table_b = __generate_url('b', currency, date_range[0], date_range[1])

        ra = requests.get(url_table_a)
        rb = requests.get(url_table_b)

        if ra.status_code == 200:
            responses.append(json.loads(ra.text))
        elif rb.status_code == 200:
            responses.append(json.loads(rb.text))

    final_result = __convert_array_of_responses(responses)
    __append_missing_dates(final_result)
    final_result = __convert_dates_to_string(final_result)

    return final_result

if __name__ == '__main__':
    eur = get_rete_of_currency('eur', 365 // 2)
    usd = get_rete_of_currency('usd', 365 // 2)
    print(len(eur))
    print(len(usd))

    # print(json.dumps(eur, indent=4))
    # print(json.dumps(usd, indent=4))
