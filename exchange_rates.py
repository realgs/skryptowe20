import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

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

def __plot_chart(usd_exchange_rate, eur_exchange_rate):
    plt.title('Zaleznosc ceny euro i dolara')
    plt.ylabel('Kurs w zlotowkach')
    plt.xticks(rotation=270)
    plt.xlabel('Data')
    
    usd_data = __extract_from_exchange_rate(usd_exchange_rate)
    legend_usd,=plt.plot(usd_data[0], usd_data[1], color ='green', label = 'USD')
    eur_data = __extract_from_exchange_rate(eur_exchange_rate)
    legend_eur,=plt.plot(eur_data[0], eur_data[1], color='red', label = 'EUR')
    plt.legend(handles=[legend_usd,legend_eur])

    current_axes = plt.gca() 
    current_axes.set_xlim(left=0)
    current_axes.xaxis.set_major_locator(MultipleLocator(5))
    current_axes.xaxis.set_minor_locator(MultipleLocator(1))

    current_axes.yaxis.set_major_locator(MultipleLocator(0.1))
    current_axes.yaxis.set_minor_locator(MultipleLocator(0.05))
    plt.show()

def __extract_from_exchange_rate(exchange_rate):
    exchange_rate_without_header = exchange_rate[1:]
    days = [t[0] for t in exchange_rate_without_header]
    rates = [t[1] for t in exchange_rate_without_header]
    return (days, rates)

if __name__ == "__main__":
    usd_exchange_rate = __get_average_exchange_rate('usd', 180)
    #__print_exchange_rate(usd_exchange_rate)
    eur_exchange_rate = __get_average_exchange_rate('eur', 180)
    #__print_exchange_rate(eur_exchange_rate)
    __plot_chart(usd_exchange_rate, eur_exchange_rate)
