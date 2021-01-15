from datetime import datetime, timedelta, date
import requests

DATE_FORMAT = '%Y-%m-%d'
LINK = "http://api.nbp.pl/api/exchangerates/rates/a"
HALF_YEAR = 183
API_DAYS_LIMIT = 367
US_DOLLAR = 'USD'


def request_url(currency, start_date, end_date=None):
    url = f"{LINK}/{currency}/{date_to_str(start_date)}/{date_to_str(end_date)}"
    resp = requests.get(url)

    if resp.status_code == 404:
        return None
    elif resp.status_code != 200:
        raise requests.exceptions.RequestException(f"{url} returned {resp.status_code} {resp.text}")

    return resp.json()


def divide_periods(start_date, end_date):
    start_date = to_date(start_date)
    end_date = to_date(end_date)

    periods = []
    total_days = (end_date - start_date).days

    while total_days >= 0:
        period_length = min(total_days, API_DAYS_LIMIT)
        end_date = start_date + timedelta(period_length)
        periods.append((start_date, end_date))
        start_date = end_date + timedelta(1)
        total_days -= period_length + 1

    return periods


def repair_data(start_date, end_date, data, currency):
    start_date = to_date(start_date)
    end_date = to_date(end_date)

    i = 1
    repaired = False
    total_days = (end_date - start_date).days

    if not data or data[0][0] != start_date:
        while not repaired:
            resp = request_url(currency, start_date - timedelta(i))
            if resp:
                data.insert(0, (start_date, resp['rates'][0]['mid'], True))
                repaired = True
            else:
                i += 1

    i = 0
    while len(data) < total_days - 1:
        if data[i][0] + timedelta(1) != data[i + 1][0]:
            data.insert(i + 1, (data[i][0] + timedelta(1), data[i][1], True))
        i += 1


def to_date(date):
    if isinstance(date, datetime):
        return date
    else:
        return datetime.strptime(date, DATE_FORMAT)


def date_to_str(date):
    if date is None:
        return ""
    elif isinstance(date, str):
        return date
    else:
        return datetime.strftime(date, DATE_FORMAT)


def get_currency_between_dates(currency, start_date, end_date):
    data = []
    periods = divide_periods(start_date, end_date)

    for period in periods:
        resp = request_url(currency, period[0], period[1])
        if resp:
            for rate in resp['rates']:
                data.append((to_date(rate['effectiveDate']), rate['mid'], False))

    repair_data(start_date, end_date, data, currency)
    return data
