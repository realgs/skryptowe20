import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import json


def fetch_avg_currency(table='a', prev_date='2012-01-01', curr_date='2012-01-31', currency='usd'):
    req = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{prev_date}/{curr_date}")
    if req.status_code == 200:
        res = req.json()
        return res
    else:
        return json.loads('{}')


def fetch_currency_from_two_tables( prev_date='2012-01-01', curr_date='2012-01-31', currency='usd'):
    tab_a = fetch_avg_currency(prev_date=prev_date, curr_date=curr_date, currency=currency)
    tab_b = fetch_avg_currency(table='b', prev_date=prev_date, curr_date=curr_date, currency=currency)

    return from_json_to_list(tab_a) + from_json_to_list(tab_b)


def print_json(json_file):
    print(json.dumps(json_file, indent=4, sort_keys=True))


def plot(x1, y1, x2, y2, label1='', label2='', xlabel='', ylabel='', title=''):
    fig, ax = plt.subplots()
    ax.plot(x1,y1, label=label1)
    ax.plot(x2, y2, label=label2)
    ax.set(xlabel=xlabel, ylabel=ylabel,
            title=title)
    ax.set_xticks(x1[::10])
    ax.legend()
    plt.xticks(rotation=40)
    fig.savefig(f'plots/{title}.svg')
    plt.show()


def from_json_to_list(json_file):
    print_json(json_file)
    if 'rates' in json_file:
        mids = [x['mid'] for x in json_file['rates']]
        dates = [x['effectiveDate'] for x in json_file['rates']]
        return list(zip(mids, dates))
    else:
        return []


if __name__ == "__main__":
    date1 ='2020-05-01'
    date2 = '2020-11-20'

    avg_usd = fetch_currency_from_two_tables(date1, date2)
    usd_mids = [x[0] for x in avg_usd]
    usd_dates = [x[1] for x in avg_usd]

    avg_euro = fetch_currency_from_two_tables(date1, date2, 'eur')
    euro_mids = [x[0] for x in avg_euro]
    euro_dates = [x[1] for x in avg_euro]

    plot(
        usd_dates,
        usd_mids,
        euro_dates,
        euro_mids,
        'USD',
        'EUR',
        xlabel='days',
        ylabel='avg currency',
        title=f'Average currency values (EUR, USD) from {date1} to {date2}'
    )
