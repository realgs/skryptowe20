import requests
from datetime import date, timedelta
import matplotlib.pyplot as plt

TODAY_DATE = date.today()
HALF_YEAR_DAYS = 20
DOLLAR = "USD"
EURO = "EUR"

def get_avg_ex_rate(currency, days_number):
    records_number = 0
    current_date = TODAY_DATE
    result = {}
    while(records_number<days_number):
        resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/{}/{}/'.format(currency, current_date.strftime("%Y-%m-%d")))
        if resp.status_code != 200:
            pass
        else:
            result[current_date.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']
            records_number += 1
        current_date = current_date - timedelta(days=1)
    return result

def get_dollar_euro_half_year():
    dollars = {}
    euros = {}
    start_date = (TODAY_DATE - timedelta(days=HALF_YEAR_DAYS)).strftime("%Y-%m-%d")
    end_date = TODAY_DATE.strftime("%Y-%m-%d")

    resp_dollars = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/{}/{}/{}/'.format(DOLLAR, start_date, end_date))
    resp_euros = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/{}/{}/{}/'.format(EURO, start_date, end_date))

    if resp_dollars.status_code != 200:
            pass
    else:
        for record in resp_dollars.json()['rates']:
            dollars[str(record['effectiveDate'])] = record['mid']   

    if resp_euros.status_code != 200:
            pass
    else:
        for record in resp_euros.json()['rates']:
            euros[str(record['effectiveDate'])] = record['mid']
    
    return dollars, euros

def plot_dollar_euro(dollar_dict, euro_dict):
    dollar_dates = []
    dollar_rates = []
    euro_dates = []
    euro_rates = []

    for key, value in dollar_dict.items():
        dollar_dates.append(key)
        dollar_rates.append(value)

    for key, value in euro_dict.items():
        euro_dates.append(key)
        euro_rates.append(value)

    print(dollar_dates)
    print(euro_dates)
    print(dollar_rates)
    print(euro_rates)

    fig, ax = plt.subplots()
    dollar_line, = plt.plot(dollar_dates, dollar_rates, 'g', label='Dollar')
    euro_line, = plt.plot(euro_dates, euro_rates, 'r', label='Euro')
    plt.xlabel('Dates')
    ax.xaxis.set_label_coords(1.05, -0.025)
    plt.xticks(rotation=45)
    plt.xticks(fontsize=6)
    plt.ylabel('Rates')
    plt.title('Dollar and Euro rates')
    plt.legend(handles=[dollar_line, euro_line])
    plt.savefig("dol_eur_fig.svg")
    
