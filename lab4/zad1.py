import requests
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

url = 'http://api.nbp.pl/api/exchangerates/rates/a/'


def getRatesFromLastNDays(currency, days):
    now = datetime.today()
    dateDaysAgo = now - timedelta(days)
    daysArray = []
    ratesArray = []
    resp = requests.get(url + currency + '/' + dateDaysAgo.strftime('%Y-%m-%d') + '/' + now.strftime('%Y-%m-%d') + '/')
    if resp.status_code != 200:
        print('GET ' + url + currency + '/' + dateDaysAgo.strftime('%Y-%m-%d') + '/' + now.strftime(
            '%Y-%m-%d') + '/\n' '{}'.format(resp.reason))
        pass
    else:
        for rate in resp.json()['rates']:
            daysArray.append(rate['effectiveDate'])
            ratesArray.append(rate['mid'])
        return daysArray, ratesArray


def createPlot(days1, rates1, days2, rates2):
    days_short = days1[::25]
    plt.xticks(range(0, len(days1), 25), days_short)
    plt.xticks(fontsize=6)
    plt.plot(days1, rates1, label="USD")
    plt.plot(days2, rates2, label="EUR")
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.title('Rates of USD and EUR in previous half year')
    plt.legend()
    plt.savefig("eurUsdRates.svg")
    plt.show()


def halfYearUsdEurRates():
    daysUSD, ratesUSD = getRatesFromLastNDays('USD', 183)
    daysEUR, ratesEUR = getRatesFromLastNDays('EUR', 183)
    return daysUSD, ratesUSD, daysEUR, ratesEUR


def showUsdEurRates():
    days1, rates1, days2, rates2 = halfYearUsdEurRates()
    createPlot(days1, rates1, days2, rates2)
