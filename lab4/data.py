from datetime import datetime, timedelta
import requests


def get_currency_from_period(currency, date_from, date_to):
    table_type = 'a'
    resp = requests.get(
        f'http://api.nbp.pl/api/exchangerates/rates/{table_type}/{currency}/{date_from}/{date_to}/?format=json')
    if resp.status_code == 200:
        data = resp.json()['rates']
        for record in data:
            record.pop('no', None)
        return data
    print("Error with code {}".format(resp.status_code))


def get_currency_last_x_days(currency, days):
    date_to = datetime.today().strftime('%Y-%m-%d')
    date_from = (datetime.today() - timedelta(days)).strftime('%Y-%m-%d')
    output = get_currency_from_period(currency, date_from, date_to)
    return output
