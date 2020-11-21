import requests
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


sns.set()

FIGSIZE = (12, 6)
MAX_DAYS_FOR_QUERY = 93


def _url(path):
    return 'http://api.nbp.pl' + path + '/?format=json'


def get_exchange_rates(code, start_date, end_date):
    return requests.get(_url(f'/api/exchangerates/rates/a/{code}/{start_date}/{end_date}'))


def get_exchange_rate_on_date(code, date):
    return requests.get(_url(f'/api/exchangerates/rates/a/{code}/{date}'))


def get_currency_quotes(currency, start_date, end_date):
    rates = {}
    while start_date < end_date:
        query_end_date = min(start_date + datetime.timedelta(MAX_DAYS_FOR_QUERY), end_date)
        data = get_exchange_rates(currency, start_date, query_end_date)
        if data.status_code != 200:
            raise Exception("Couldn't correctly execute request.")
        else:
            for values in data.json()['rates']:
                rates[values['effectiveDate']] = values['mid']
        start_date += datetime.timedelta(MAX_DAYS_FOR_QUERY)
    return rates


def plot_usd_eur_currency_quotes(days):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)

    euro_rates = get_currency_quotes('EUR', start_date, end_date)
    usd_rates = get_currency_quotes('USD', start_date, end_date)

    plt.figure(figsize=FIGSIZE)
    plt.plot(list(euro_rates.keys()), list(euro_rates.values()), color='blue', label='Euro')
    plt.plot(list(usd_rates.keys()), list(usd_rates.values()), color='green', label='Dolar')
    plt.legend()
    plt.title('Notowania euro i dolara przez ostatnie 183 dni')
    plt.xlabel('Data')
    plt.ylabel('Kurs waluty względem PLN')
    plt.legend()
    plt.xticks(list(euro_rates.keys())[::10], rotation=25)
    plt.savefig('transactions_sum.svg', format='svg')
    plt.show()


if __name__ == "__main__":
    plot_usd_eur_currency_quotes(183)
