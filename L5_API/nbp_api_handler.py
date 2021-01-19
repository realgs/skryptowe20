import requests
from datetime import datetime, timedelta

MAX_TRIES = 10
MAX_TIME_FRAME = 365


def _url(path):
    return 'http://api.nbp.pl/api/exchangerates' + path


def currency_rates_dates_interpolated_time_frame(currency_code, date_from, date_to):
    rates = []
    dates = []
    interpolated = []

    table = _get_table(currency_code)
    if not _are_dates(date_from, date_to) or not table:
        return rates, dates

    time_frames = _split_time_frame(date_from, date_to)

    for frame in time_frames:
        date_from, date_to = frame
        request = _get_rates_request(currency_code, table, date_from, date_to)

        if request.status_code == 200:
            data = request.json()['rates']
            n = len(data)

            if data[0]['effectiveDate'] != date_from:
                rates.append(_currency_get_last_known_rate(currency_code, table, date_from))
                dates.append(date_from)
                interpolated.append(1)

            for i in range(n):
                rates.append(float(data[i]['mid']))
                dates.append(data[i]['effectiveDate'])
                interpolated.append(0)

            if dates[-1] != date_to:
                rates.append(_currency_get_last_known_rate(currency_code, table, date_to))
                dates.append(date_to)
                interpolated.append(1)

        else:
            rates.append(_currency_get_last_known_rate(currency_code, table, date_from))
            dates.append(date_from)
            interpolated.append(1)

            if date_from != date_to:
                rates.append(_currency_get_last_known_rate(currency_code, table, date_to))
                dates.append(date_to)
                interpolated.append(1)

        rates, dates, interpolated = _fill_in_missing_rates(rates, dates, interpolated)

    return rates, dates, interpolated


def currency_rates_dates_interpolated(currency_code, days):
    date_from = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    date_to = datetime.today().strftime('%Y-%m-%d')

    rates, dates, interpolated = currency_rates_dates_interpolated_time_frame(currency_code, date_from, date_to)

    return rates, dates, interpolated


def _currency_get_last_known_rate(currency_code, table, date):
    rate = 0.0
    date = datetime.strptime(date, '%Y-%m-%d')
    request_code = 0
    tries_left = MAX_TRIES

    while request_code != 200 and tries_left > 0:
        request = _get_rates_request(currency_code, table, date.date(), date.date())
        request_code = request.status_code

        if request_code == 200:
            rate = request.json()['rates'][0]['mid']

        tries_left -= 1
        date = date - timedelta(days=1)

    return rate


def _split_time_frame(date_from, date_to):
    date_frames = []

    date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
    date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
    temp_date_obj = date_from_obj

    while temp_date_obj <= date_to_obj:
        new_from = temp_date_obj
        new_to = new_from + timedelta(days=MAX_TIME_FRAME)

        if new_to > date_to_obj:
            new_to = date_to_obj

        date_frames.append((new_from.strftime('%Y-%m-%d'), new_to.strftime('%Y-%m-%d')))
        temp_date_obj = new_to + timedelta(days=1)

    return date_frames


def _fill_in_missing_rates(rates, dates, interpolated):
    first_day = datetime.strptime(dates[0], '%Y-%m-%d')
    last_day = datetime.strptime(dates[len(dates) - 1], '%Y-%m-%d')
    delta = (last_day - first_day).days

    for i in range(delta):
        date = (first_day + timedelta(days=i)).strftime('%Y-%m-%d')

        if dates[i] != date:
            dates.insert(i, date)
            rates.insert(i, rates[i - 1])
            interpolated.insert(i, 1)

    return rates, dates, interpolated


def _get_rates_request(currency_code, table, date_from, date_to):
    url = _url("/rates/{}/{}/{}/{}".format(
        table,
        currency_code,
        date_from,
        date_to
    ))
    return requests.get(url)


def _get_table(currency_code):
    for table in ['A', 'B']:
        if _check_table(currency_code, table):
            return table
    return ''


def _check_table(currency_code, table):
    url = _url("/tables/{}".format(table))
    response = requests.get(url).json()

    for rate in response[0]['rates']:
        if rate['code'] == currency_code:
            return True

    return False


def _are_dates(date_from, date_to):
    try:
        datetime.strptime(date_from, '%Y-%m-%d')
        datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        return False

    return date_from <= date_to
