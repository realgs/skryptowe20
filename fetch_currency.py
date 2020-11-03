import matplotlib.pyplot as plt
import requests
from enum import Enum
from datetime import datetime, timedelta


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    PLN = 'PLN'
    CHF = 'CHF'


def get_previous_days(currency, days):
    if currency not in Currency._value2member_map_ or days < 1:
        print('Invalid arguments, please try again')
    else:
        current_date = datetime.now()
        beginning = current_date - timedelta(days=days)
        response = requests.get(
            f'http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{beginning.date()}/{current_date.date()}/?format=json')
        if(response.status_code != 200):
            print(f'Request Error {response.status_code}')
            return response.status_code
        else:
            return response


def parse_response(response):
    y = []
    x = []
    print(response.json()['rates'][1])
    for value in response.json()['rates']:
        y.append(value['mid'])
        x.append(datetime.strptime(value['effectiveDate'], '%Y-%m-%d'))
    return x, y


def create_chart(currencies, days):
    if not currencies or days < 1:
        print('Invalid arguments, please try again')
    else:
        # current_date = datetime.today()
        # x = [str((current_date - timedelta(days=x)).date()) for x in range(days, 0, -1)]

        fig, ax = plt.subplots()

        for currency in currencies:
            response = get_previous_days(currency, days)
            if isinstance(response, int) or response is None:
                print(f'Failed fetching {currency}')
            else:
                x, y = parse_response(response)
                print(y)
                ax.plot(x, y, label=currency)

        ax.xaxis_date()
        fig.autofmt_xdate()
        plt.xlabel('Data')
        plt.ylabel('Wartosc waluty [PLN]')
        plt.legend()
        plt.savefig('currencies.eps')
        plt.show()


create_chart(['USD', 'EUR'], 183)
