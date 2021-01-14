import requests
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates

API_URL = "http://api.nbp.pl/api"
CURRENCY1 = 'USD'
CURRENCY2 = 'EUR'


def get_exchangerates(number_of_days, currency):
    end_day = date.today().strftime("%Y-%m-%d")
    start_day = date.today() - timedelta(days=number_of_days)
    print(start_day, end_day)
    get_currency_url = f'{API_URL}/exchangerates/rates/a/{currency}/{start_day}/{end_day}'
    print(get_currency_url)
    stock = requests.get(get_currency_url)
    if stock.status_code != 200:
        print(f'Request error: {stock.status_code}')
        return stock.status_code
    else:
        return stock.json()


def print_nicely(json_stock):
    print('currency : ', json_stock['currency'])
    for val in json_stock['rates']:
        print("date: ", val['effectiveDate'])
        print("average value: ", val['mid'])


def get_matplotDates_and_rates(json_stock):
    dates = []
    rates = []
    for val in json_stock['rates']:
        rates.append(val['mid'])
        dates.append(matplotlib.dates.date2num(datetime.strptime(val['effectiveDate'], '%Y-%m-%d')))
    return rates, dates


if __name__ == '__main__':
    print_nicely(get_exchangerates(10, CURRENCY1))
    # ------------------------------------------------------
    usd_rates, usd_dates = get_matplotDates_and_rates(get_exchangerates(182, CURRENCY1))
    eur_rates, eur_dates = get_matplotDates_and_rates(get_exchangerates(182, CURRENCY2))
    plt.plot_date(usd_dates, usd_rates, '-', linestyle='solid', xdate=True, label=CURRENCY1)
    plt.plot_date(eur_dates, eur_rates, '-', xdate=True, label=CURRENCY2)
    plt.xlabel('Date')
    plt.ylabel('Average rate')
    plt.title(f'Exchange rates ({CURRENCY1}, {CURRENCY2}) from last 6 mothns')
    plt.legend()
    plt.savefig('test.svg')
    plt.show()
