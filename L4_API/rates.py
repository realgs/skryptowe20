import requests
from datetime import datetime, timedelta


def currency_rates(currency_code, days):
    rates = []
    table = get_table(currency_code)

    if days > 255 or days < 1 or table is None:
        return rates

    url = "http://api.nbp.pl/api/exchangerates/rates/" + table + "/" + currency_code \
          + "/" + (datetime.today() - timedelta(days=days-1)).strftime('%Y-%m-%d') \
          + "/" + datetime.today().strftime('%Y-%m-%d') + "/"
    request = requests.get(url).json()['rates']
    n = len(request)

    for i in range(n):
        rates.append(float(request[i]['mid']))

    return rates


def get_table(currency):
    for table in ['A', 'B']:
        if check_table(currency, table):
            return table
    return None


def check_table(currency, table):
    found = False
    url = "http://api.nbp.pl/api/exchangerates/tables/" + table + "/today/"
    response = requests.get(url).text

    if currency in response:
        found = True

    return found


if __name__ == '__main__':
    print(currency_rates('USD', 182))
    print(currency_rates('EUR', 182))
