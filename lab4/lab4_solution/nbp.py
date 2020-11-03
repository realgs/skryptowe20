import requests
from datetime import date, timedelta

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

    
