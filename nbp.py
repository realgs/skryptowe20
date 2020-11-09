import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import json

def fetch_avg_currency(currency="usd", days=10):
       req = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/last/{days}/?format=json")
       res = req.json()
       return res


def print_json(json_file):
       print(json.dumps(json_file, indent=4, sort_keys=True))


def plot(x1, y1, x2, y2, xlabel='', ylabel='', title=''):
       fig, ax = plt.subplots()
       ax.plot(x1,y1)
       ax.plot(x2, y2)
       ax.set(xlabel=xlabel, ylabel=ylabel,
              title=title)
       ax.set_xticks(x1[::10])
       plt.xticks(rotation=40)
       fig.savefig(f'plots/{title}.svg')
       plt.show()


avg_usd = fetch_avg_currency(days=182)
avg_euro = fetch_avg_currency('eur', 182)
print_json(avg_usd)
print_json(avg_euro)

usd_mids = [x['mid'] for x in avg_usd['rates']]
usd_dates = [x['effectiveDate'] for x in avg_usd['rates']]

euro_mids = [x['mid'] for x in avg_euro['rates']]
euro_dates = [x['effectiveDate'] for x in avg_euro['rates']]

plot(
       usd_dates,
       usd_mids,
       euro_dates,
       euro_mids,
       xlabel='days',
       ylabel='avg currency',
       title='Average currency values (EUR, USD) in 182 days'
       )
