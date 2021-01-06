import sqlite3
import requests
import calendar
import datetime


def __call_api(currency, start_date_string, end_date_string):
    requestUrl = 'http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/{}/'.format(currency, start_date_string,
                                                                                end_date_string)
    response = requests.get(requestUrl)
    if response.status_code == 400:
        return [('Error', 'Sformulowano niepoprawne zapytanie')]
    if response.status_code == 404:
        return [('Error', 'Brak danych dla waluty {} danego zakresu czasowego'.format(currency))]

    response_json = response.json()
    result = []
    for rate in response_json['rates']:
        result.append((rate['effectiveDate'], rate['mid']))
    return result


def format_date(date):
    return date.strftime('%Y-%m-%d')


def __find_first_previous_rate(currency, date):
    offset = 1
    while True:
        new_date = date - datetime.timedelta(days=offset)
        rate = __call_api(currency, new_date, new_date)
        if rate[0][0] != 'Error':
            return rate[0][1]
        offset = offset + 1
        if offset > 30:
            print('Nie znaleziono danych waluty w ostatnich 30 dniach!')
            return 0


def __get_exchange_rate(currency, start_date, end_date):
    exchange_rate = __call_api(currency, format_date(start_date), format_date(end_date))
    delta = datetime.timedelta(days=1)
    result = []

    if format_date(start_date) != exchange_rate[0][0]:
        result.append((format_date(start_date), __find_first_previous_rate(currency, start_date)))
        start_date += delta

    index = 0
    while start_date <= end_date:
        formatted_date = format_date(start_date)
        if index < len(exchange_rate) and formatted_date == exchange_rate[index][0]:
            result.append((formatted_date, exchange_rate[index][1]))
            index = index + 1
        else:
            result.append((formatted_date, exchange_rate[index - 1][1]))
        start_date += delta
    return result


def __get_all_exchange_rates_in_string():
    all_rates = []
    years = [2009, 2010]
    for y in years:
        for i in range(3):
            start = datetime.date(y, 4 * i + 1, 1)
            end = datetime.date(y, 4 * (i + 1), calendar.monthrange(y, 4 * (i + 1))[1])
            rate = __get_exchange_rate('usd', start, end)
            all_rates.append(rate)

    string_rate = str(all_rates[0])[1:-1]
    for rate in all_rates[1:]:
        string_rate = string_rate + ','
        string_rate = string_rate + str(rate)[1:-1]
    return string_rate


if __name__ == '__main__':
    rates = __get_all_exchange_rates_in_string()

    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    c.execute('CREATE TABLE exchange_rate(date text, price real)')
    c.execute('INSERT INTO exchange_rate VALUES {}'.format(rates))
    conn.commit()
    conn.close()