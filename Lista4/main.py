import requests
import datetime
import matplotlib.pyplot as plt


# Zadanie 1 - funkcja pobierająca średnie kursy notowań wybranej waluty z ostatnich X dni
def get_average_currency_rates(currency, days):
    url = 'http://api.nbp.pl/api/exchangerates/rates/A/' + currency + '/'
    result = []
    end_date = datetime.date.today()

    while days > 0:
        begin_date = end_date - datetime.timedelta(days=min(days, 92))
        response = requests.get(url + begin_date.strftime('%Y-%m-%d') + '/' + end_date.strftime('%Y-%m-%d'))
        if response.status_code == 200:
            result = response.json()['rates'] + result
        days -= 93
        end_date = end_date - datetime.timedelta(days=93)

    return result


#Zadanie 3 - Rysowanie wykresu
def draw_currency_diagram(dollar_data, euro_data):
    data_time = []
    data_dollar = []
    data_euro = []

    for i in range(len(dollar_data)):
        data_time.append(dollar_data[i]['effectiveDate'])
        data_dollar.append(dollar_data[i]['mid'])
        data_euro.append(euro_data[i]['mid'])

    plt.title('Kursy dolara (USD) i euro (EUR) z ostatnich 183 dni')
    plt.xlabel('Data')
    plt.ylabel('Kurs względem PLN')
    plt.xticks(range(len(data_time))[::10], rotation=35)

    plt.plot(data_time, data_dollar, label='USD')
    plt.plot(data_time, data_euro, label='EUR')
    plt.legend()
    plt.savefig('currency_rates.svg', format='svg')
    plt.show()


if __name__ == '__main__':
    # Zadanie 2 - przykładowe wywołanie funkcji
    half_year_dollar_averages = get_average_currency_rates('USD', 183)
    half_year_euro_averages = get_average_currency_rates('EUR', 183)

    draw_currency_diagram(half_year_dollar_averages, half_year_euro_averages)
