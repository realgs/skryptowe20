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


avg_usd = fetch_avg_currency(days=182)
avg_euro = fetch_avg_currency('eur', 182)
print_json(avg_usd)
print_json(avg_euro)
