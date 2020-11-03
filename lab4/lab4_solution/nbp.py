import requests
from datetime import date, timedelta

TODAY_DATE = date.today()

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

    
