import datetime
import json

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests


# exercise 1----------------------------------------------------------------------------
def get_currency_exchange_rates(currency: str, X: int):
    today_date = datetime.date.today()
    x__days_ago_date = today_date - datetime.timedelta(days=X - 1)
    data = requests.get(r'http://api.nbp.pl/api/exchangerates/rates/a/' + currency + '/' + str(x__days_ago_date) + '/' + str(today_date) + '/')
    data_len = len(json.loads(data.text)['rates'])
    exchange_rates = [json.loads(data.text)['rates'][i]['mid'] for i in range(data_len)]
    nbp_dates = [json.loads(data.text)['rates'][i]['effectiveDate'] for i in range(data_len)]
    all_dates = [str(x__days_ago_date + datetime.timedelta(days=i)) for i in range(X)]

    # complete empty dates for weekends
    for i in range(len(all_dates)):
        if i >= len(nbp_dates):
            exchange_rates.insert(i, exchange_rates[i - 1])
            nbp_dates.insert(i, all_dates[i])
        elif all_dates[i] != nbp_dates[i]:
            exchange_rates.insert(i, exchange_rates[i])
            nbp_dates.insert(i, all_dates[i])

    return exchange_rates


# exercise 2----------------------------------------------------------------------------
# half a year - 183 days
dollar = get_currency_exchange_rates('usd', 183)
euro = get_currency_exchange_rates('eur', 183)

# exercise 3----------------------------------------------------------------------------
today_date = datetime.date.today()
x__days_ago_date = today_date - datetime.timedelta(days=len(dollar))
days = mdates.drange(x__days_ago_date, today_date, datetime.timedelta(days=1))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=20))
plt.plot(days, dollar, days, euro)
plt.gcf().autofmt_xdate()

plt.xlabel('czas')
plt.ylabel('średni kurs notowań [zł]')
plt.title('Zależność notowań dolara i euro od czasu')
plt.legend(['USD', 'EUR'], loc='best')
plt.savefig('dollar_euro_exchange_rates_chart.svg')
plt.show()
