import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from datetime import datetime, timedelta


LIMIT = 360 #api limit in days


def fetch_avg_currency(table='a', prev_date='2012-01-01', curr_date='2012-01-31', currency='usd'):
    dates = get_dates(prev_date, curr_date)
    result = []
    for pair in list(zip(dates[:-1], dates[1:])):
        req = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{pair[0]}/{pair[1]}")
        if req.status_code == 200:
            res = from_json_to_list(req.json())
            result += res

    return result


def get_dates(start, end):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    days_left = (end - start).days
    date = start
    dates = [start]

    while days_left > 0:
        date += timedelta(days=min(LIMIT, days_left))
        dates.append(date)

        days_left -= (min(LIMIT, days_left) + 1)
    return [x.strftime('%Y-%m-%d') for x in dates]


def fetch_currency_from_two_tables(prev_date='2012-01-01', curr_date='2012-01-31', currency='usd'):
    tab_a = fetch_avg_currency(prev_date=prev_date, curr_date=curr_date, currency=currency)
    tab_b = fetch_avg_currency(table='b', prev_date=prev_date, curr_date=curr_date, currency=currency)

    return tab_a + tab_b


def plot(x1, y1, x2, y2, label1=' ', label2=' ', xlabel=' ', ylabel=' ', title=' '):
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.15)
    ax.plot(x1, y1, label=label1)
    ax.plot(x2, y2, label=label2)
    ax.set(xlabel=xlabel, ylabel=ylabel,
            title=title)
    ax.set_xticks(ax.get_xticks()[::len(ax.get_xticks()) // 4])
    ax.legend()
    plt.xticks(rotation=20)
    fig.savefig(f'plots/{title}.svg')
    plt.show()


def from_json_to_list(json_file):
    if 'rates' in json_file:
        mids = [x['mid'] for x in json_file['rates']]
        dates = [x['effectiveDate'] for x in json_file['rates']]
        return list(zip(mids, dates))
    else:
        return []


if __name__ == "__main__":
    date1 ='2020-05-01'
    date2 = '2020-11-15'

    avg_usd = fetch_currency_from_two_tables(date1, date2)
    usd_mids, usd_dates = zip(*avg_usd)

    avg_euro = fetch_currency_from_two_tables(date1, date2, 'eur')
    euro_mids, euro_dates = zip(*avg_euro)

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
