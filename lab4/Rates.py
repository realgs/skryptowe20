import requests
import PlotRates
from datetime import date, timedelta


def get_rates(currency, days):
    processed_requests = 0
    date_to_use = date.today()
    result = {}
    while processed_requests < days:
        resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/{}/{}/{}/'.format("A", currency,
                                                                                         date_to_use.strftime(
                                                                                             "%Y-%m-%d")))
        if resp.status_code != 200:
            pass
            # print("Data request wasn't successful, status_code:{}", resp.status_code)
        else:
            result[date_to_use.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']
            processed_requests += 1
        date_to_use -= timedelta(days=1)
    return result


usd = get_rates("USD", 180)
eur = get_rates("EUR", 180)
PlotRates.plot_dollar_euro(usd, eur)
