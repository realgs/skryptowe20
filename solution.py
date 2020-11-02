import requests
import matplotlib.pyplot as plt

API_LINK = 'http://api.nbp.pl/api'

def getExchangeRates(currency, days):
    global API_LINK
    url = '{}/exchangerates/rates/a/{}/last/{}'.format(API_LINK, currency, days)
    resp = requests.get(url)
    if resp.status_code != 200:
         raise Exception('GET {} returned code: {}'.format(url, resp.status_code))
    return resp.json()

def get_exchange_rates_and_dates(rates):
    rates_list = []
    dates = []
    for r in rates:
        rates_list.append(r['mid'])
        dates.append(r['effectiveDate'])
    return (dates, rates_list)

euro_rates = getExchangeRates('eur', 182)
usd_rates = getExchangeRates('usd', 182)
euro_rates_and_dates = get_exchange_rates_and_dates(euro_rates['rates'])
usd_rates_and_dates = get_exchange_rates_and_dates(usd_rates['rates'])
fig = plt.figure()
fig.set_size_inches(15,10)
plt.plot(euro_rates_and_dates[0], euro_rates_and_dates[1], label="Kurs euro")
plt.plot(usd_rates_and_dates[0], usd_rates_and_dates[1], label="Kurs dolara amerykańskiego")
plt.title("Kursy euro oraz dolara amerykańskiego z ostatnich 6 miesięcy")
plt.axes().xaxis.set_major_locator(plt.MaxNLocator(25))
plt.xticks(rotation=45, ha="right")
plt.xlabel("Dzień")
plt.ylabel("Kurs waluty")
plt.legend()
plt.tight_layout()
plt.savefig('wykres.svg', format='svg', dpi=1800)
plt.show()
