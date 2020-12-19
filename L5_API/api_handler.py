import requests
from datetime import datetime, timedelta


def currency_rates_dates_interpolated(currency_code, days):
    date_from = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    date_to = datetime.today().strftime('%Y-%m-%d')

    rates, dates, interpolated = currency_rates_dates_interpolated_time_frame(currency_code, date_from, date_to)

    return rates, dates, interpolated


def currency_rates_dates_interpolated_time_frame(currency_code, date_from, date_to):
    rates = []
    dates = []

    time_frames = __split_time_frame(date_from, date_to)

    for frame in time_frames:
        date_from, date_to = frame
        url = __url("api/exchangerates/rates/{}/{}/{}/{}/".format(
            __get_table(currency_code),
            currency_code,
            date_from,
            date_to))

        request = requests.get(url)
        if request.status_code == 200:
            data = request.json()['rates']
            n = len(data)

            for i in range(n):
                rates.append(float(data[i]['mid']))
                dates.append(data[i]['effectiveDate'])

    rates, dates, interpolated = __fill_in_missing_rates(rates, dates)

    return rates, dates, interpolated


def __split_time_frame(date_from, date_to):
    date_frames = []

    try:
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
        temp_date_obj = date_from_obj

        while temp_date_obj < date_to_obj:
            if temp_date_obj.weekday() == 5:
                temp_date_obj = temp_date_obj - timedelta(days=1)
            elif temp_date_obj.weekday() == 6:
                temp_date_obj = temp_date_obj - timedelta(days=2)

            new_from = temp_date_obj
            new_to = new_from + timedelta(days=366)

            if new_to > date_to_obj:
                new_to = date_to_obj

            date_frames.append((new_from.strftime('%Y-%m-%d'), new_to.strftime('%Y-%m-%d')))
            temp_date_obj = new_to + timedelta(days=1)
    except ValueError as e:
        print('api_handler: split_time_frame: ' + str(e))

    return date_frames


def __fill_in_missing_rates(rates, dates):
    interpolated = []

    if len(rates) > 1:
        first_day = datetime.strptime(dates[0], '%Y-%m-%d')
        last_day = datetime.strptime(dates[len(dates) - 1], '%Y-%m-%d')

        delta = (last_day - first_day).days

        for i in range(delta + 1):
            date = (first_day + timedelta(days=i)).strftime('%Y-%m-%d')

            if dates[i] != date:
                dates.insert(i, date)
                rates.insert(i, rates[i - 1])
                interpolated.append(1)
            else:
                interpolated.append(0)

    return rates, dates, interpolated


def __get_table(currency):
    for table in ['A', 'B']:
        if __check_table(currency, table):
            return table
    return ''


def __check_table(currency, table):
    found = False
    url = __url("api/exchangerates/tables/{}/last/1/".format(table))
    response = requests.get(url).text

    if currency != '' and currency in response:
        found = True

    return found


def __url(path):
    return 'http://api.nbp.pl/' + path


if __name__ == '__main__':
    date_from = '2009-01-02'
    date_to = '2014-12-31'

    dates, rates, interpolated = currency_rates_dates_interpolated_time_frame('USD', date_from, date_to)
    print(len(dates))
    print(len(rates))
    print(len(interpolated))
