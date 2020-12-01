import requests
from datetime import date, timedelta
import matplotlib.pyplot as plt

TODAY_DATE = date.today()
HALF_YEAR_DAYS = 183
STATUS_OK = 200
USD = 'USD'
EUR = 'EUR'


def get_avg_quot_rate(currency, days_number):
    records_saved = 0
    current_date = TODAY_DATE
    result = {}
    while records_saved < days_number:
        date_format = current_date.strftime("%Y-%m-%d")
        resp = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/A/{currency}/{date_format}/")
        if resp.status_code == STATUS_OK:
            result[date_format] = resp.json()['rates'][0]['mid']
        else:
            print("Brak danych z API " + current_date.strftime("%Y-%m-%d"))
        records_saved += 1
        current_date = current_date - timedelta(days=1)
    return result


def get_dollar_euro_half_year():
    dollars = get_avg_quot_rate(USD, HALF_YEAR_DAYS)
    euros = get_avg_quot_rate(EUR, HALF_YEAR_DAYS)

    return dollars, euros


def plot_dollar_euro(dollar_data, euro_data):
    dollar_dates = []
    dollar_rates = []
    euro_dates = []
    euro_rates = []

    for date, rate in dollar_data.items():
        dollar_dates.append(date)
        dollar_rates.append(rate)
    dollar_rates.reverse()
    dollar_dates.reverse()

    for date, rate in euro_data.items():
        euro_dates.append(date)
        euro_rates.append(rate)
    euro_dates.reverse()
    euro_rates.reverse()

    plt.figure(figsize=(16, 7))
    dollar_line, = plt.plot(dollar_dates, dollar_rates, 'r', label='Dollar')
    euro_line, = plt.plot(euro_dates, euro_rates, 'b', label='Euro')
    plt.xticks(range(0, len(dollar_dates), 5), dollar_dates[::5], rotation=45, fontsize=10)
    plt.xlabel('Dates')
    plt.ylabel('Rates')
    plt.title('Dollar and Euro rates')
    plt.legend(handles=[dollar_line, euro_line])
    plt.savefig("exercise3_label.svg")


dollars, euro = get_dollar_euro_half_year()
plot_dollar_euro(dollars, euro)
