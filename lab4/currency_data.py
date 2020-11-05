import requests
import json
from spyder.utils.external.github import ApiError


# address = 'http://api.nbp.pl/api/exchangerates/tables/C/'


def get_data(address) -> requests.Response:
    response = requests.get(address)

    if response.status_code != 200:
        raise ApiError(f'GET error, response status: {response.status_code}')

    return response


def get_currency_rates(symbol: str, days: int):
    address = 'http://api.nbp.pl/api/exchangerates/rates/a/' + symbol + '/last/' + str(days) + '/'
    data = get_data(address)

    with open('chfRates.json', 'w') as file:
        json.dump(data.json(), file)

    print(f'{data.json()}')


if __name__ == '__main__':
    get_currency_rates('CHF', 600)
