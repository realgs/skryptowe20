import requests

def __get_average_exchange_rate(currency, days):
    if(days < 1 or 255 < days):
        return [('Error', 'Liczba dni musi byc pomiedzy 1 a 255')]
    requestUrl = 'http://api.nbp.pl/api/exchangerates/rates/a/{}/last/{}/?format=json'.format(currency, days);
    response = requests.get(requestUrl)
    
    if response.status_code == 400:
        return [('Error', 'Sformulowano niepoprawne zapytanie')]
    if response.status_code == 404:
        return [('Error', 'Brak danych dla waluty {} danego zakresu czasowego'.format(currency))]

    response_json = response.json()
    
    result = []
    result.append((response_json['code'], response_json['currency']))
    for rate in response_json['rates']:
        result.append((rate['effectiveDate'], rate['mid']))
    return result

def __print_exchange_rate(exchange_rate):
    if(exchange_rate[0][0] != 'Error'):
        print('Nazwa waluty: {}'.format(exchange_rate[0][1]))
        for (date, value) in exchange_rate[1:][::-1]:
            print('Data: {}. Kurs {}'.format(date, value))
    else:
        print('Blad pobierania kursu waluty! Powod bledu: {}'.format(usd_exchange_rate[0][1]))

if __name__ == "__main__":
    usd_exchange_rate = __get_average_exchange_rate('usd', 180)
    #__print_exchange_rate(usd_exchange_rate)
    eur_exchange_rate = __get_average_exchange_rate('eur', 180)
    #__print_exchange_rate(eur_exchange_rate)
