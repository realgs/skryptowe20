import requests
import matplotlib.pyplot as plt
from enum import Enum
import json
from datetime import datetime, timedelta, date
from database_operations import populate_exchange_rates_table, create_exchange_rates_table

RATES_URL = 'http://api.nbp.pl/api/exchangerates/rates'
REQUEST_DAYS_LIMIT = 93
DATE_FORMAT = "%Y-%m-%d"
class ChartData():
    RATES_PLOT_NAME = 'chart.svg'
    PLOT_FORMAT = 'svg'
    PLOT_DPI = 1800


class Currencies(Enum):
    EUR = 'eur'
    USD = 'usd'
    GBP = 'gbp'
    CHF = 'chf'


def get_exchange_rates(currency, days):
    if currency in Currencies._value2member_map_ and 0 < days < 366:
        url = '{}/a/{}/last/{}'.format(RATES_URL, currency, days)
        resp = requests.get(url)
    if resp.status_code != 200:
        print('GET {} returned code: {}'.format(url, resp.status_code))
        return json.dumps({'Error code': resp.status_code})
    return resp.json()


def get_exchange_rates_range(currency, end_date, start_date):
    if currency in Currencies._value2member_map_:
        url = '{}/a/{}/{}/{}'.format(RATES_URL, currency, start_date, end_date)
        resp = requests.get(url)
        if resp.status_code == 404:
            return None
        if resp.status_code != 200:
            print('GET {} returned code: {}'.format(url, resp.status_code))
            return json.dumps({'Error code': resp.status_code})
    return resp.json()


def partition_date_range(end_date, start_date):
    if (end_date - start_date).days < REQUEST_DAYS_LIMIT +1:
        return [(end_date.strftime(DATE_FORMAT), start_date.strftime(DATE_FORMAT))]
    else:
        partitions = []
        temp_end_date = end_date
        while temp_end_date >= start_date:
            delta = timedelta(days=REQUEST_DAYS_LIMIT)
            if temp_end_date - delta >= start_date:
                partitions.append((temp_end_date.strftime(DATE_FORMAT), (temp_end_date - delta).strftime(DATE_FORMAT)))
                temp_end_date = temp_end_date - delta
            else:
                partitions.append((temp_end_date.strftime(DATE_FORMAT), start_date.strftime(DATE_FORMAT)))
                temp_end_date = temp_end_date - delta
        partitions = partitions[::-1]
        return partitions

def get_rates_for_timeframe(currency, end_date, start_date):
    corrected_rates = []
    corrected_dates = [] 
    partitions = []
    last_rate = 0
    if currency in Currencies._value2member_map_:
        partitions = partition_date_range(end_date, start_date)
        for partition in partitions:
            resp = get_exchange_rates_range(currency, partition[0], partition[1])
            if resp is not None:
                data = pull_data_from_response(resp['rates'])
                if corrected_rates != []:
                    last_rate = corrected_rates[len(corrected_rates) - 1][len(corrected_rates[len(corrected_rates) - 1]) - 1]
                corrected_data = fill_missing_exchange_rates(data, partition, last_rate)
                corrected_rates.append(corrected_data[1])
                corrected_dates.append(corrected_data[0])
    return (corrected_dates, corrected_rates)

def fill_missing_exchange_rates(data, partition, last_rate):
    dates = data[0]
    rates = data[1]
    new_rates = []
    new_dates = []
    for i in range(len(dates) - 1):
            if dates[i] not in new_dates:
                new_dates.append(dates[i])
                new_rates.append(rates[i])
            difference = (datetime.strptime(dates[i + 1], DATE_FORMAT) - datetime.strptime(dates[i], DATE_FORMAT)).days
            if difference > 1:
                for j in range(difference-1):
                    new_dates.append((datetime.strptime(dates[i], DATE_FORMAT) + timedelta(j+1)).strftime(DATE_FORMAT))
                    new_rates.append(rates[i])
            else:
                new_dates.append(dates[i+1])
                new_rates.append(rates[i+1])
    if dates[len(dates) - 1] not in new_dates:
        new_rates.append(rates[len(rates) - 1])
    begin_diff = (datetime.strptime(dates[0], DATE_FORMAT) - datetime.strptime(partition[1], DATE_FORMAT)).days
    if begin_diff > 0:
        first_date = new_dates[0]
        for i in range(begin_diff):
            new_dates.insert(0, (datetime.strptime(first_date, DATE_FORMAT) - timedelta(i+1)).strftime(DATE_FORMAT))
            new_rates.insert(0, last_rate)
    end_diff = (datetime.strptime(partition[0], DATE_FORMAT) - datetime.strptime(new_dates[len(new_dates)-1], DATE_FORMAT)).days
    if end_diff > 0:
        last_date = new_dates[len(new_dates) - 1]
        for i in range(end_diff):
            new_dates.insert(len(new_dates), (datetime.strptime(last_date, DATE_FORMAT) + timedelta(i+1)).strftime(DATE_FORMAT))
            new_rates.insert(len(new_rates), new_rates[len(new_rates)-1])
    return (new_dates, new_rates)

def fill_exchange_rates_table(data):
    create_exchange_rates_table()
    dates = data[0]
    rates = data[1]
    for i in range(len(dates)):
        rates_and_dates = list(zip(dates[i], rates[i]))
        populate_exchange_rates_table(rates_and_dates)
    

def pull_data_from_response(rates):
    rates_list = []
    dates = []
    for r in rates:
        rates_list.append(r['mid'])
        dates.append(r['effectiveDate'])
    return (dates, rates_list)


def rotate_plot_labels(plot, axis, degrees, side):
    if (axis is 'x'):
        plot.xticks(rotation=degrees, ha=side)
    elif (axis is 'y'):
        plot.yticks(rotation=degrees, ha=side)


def draw_exchange_rates_chart(currencies, days):
    rates_and_dates = []
    for curr in currencies:
        response = get_exchange_rates(curr, days)
        if response is not None:
            data = pull_data_from_response(response['rates'])
            rates_and_dates.append(data)
    fig = plt.figure()
    fig.set_size_inches(15, 10)
    for i in range(len(rates_and_dates)):
        plt.plot(rates_and_dates[i][0], rates_and_dates[i]
                 [1], label="Kurs " + currencies[i].upper())
    plt.title(f"Kursy walut na przestrzeni ostatnich {days} dni")
    plt.axes().xaxis.set_major_locator(plt.MaxNLocator(25))
    rotate_plot_labels(plt, 'x', 45, 'right')
    plt.xlabel("Dzień")
    plt.ylabel("Kurs waluty")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ChartData.RATES_PLOT_NAME,
                format=ChartData.PLOT_FORMAT, dpi=ChartData.PLOT_DPI)
    plt.show()


#draw_exchange_rates_chart(['usd', 'eur'], 180)
data = get_rates_for_timeframe('eur', datetime.strptime('2005-12-31', DATE_FORMAT), datetime.strptime('2003-12-29', DATE_FORMAT))
fill_exchange_rates_table(data)
