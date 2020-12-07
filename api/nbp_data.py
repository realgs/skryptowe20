import json
from datetime import datetime, timedelta, date
from manage_db import *
import requests

RATES_URL = 'http://api.nbp.pl/api/exchangerates/rates'
REQUEST_DAYS_LIMIT = 367
DATE_FORMAT = "%Y-%m-%d"
DB_DATE_FORMAT = "%m/%d/%Y"

class Currencies(Enum):
    EUR = 'eur'
    USD = 'usd'
    GBP = 'gbp'
    CHF = 'chf'

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
    if (end_date - start_date).days < REQUEST_DAYS_LIMIT:
        return [(end_date.strftime(DATE_FORMAT), start_date.strftime(DATE_FORMAT))]
    else:
        partitions = []
        temp_end_date = end_date
        while temp_end_date >= start_date:
            delta = timedelta(days=REQUEST_DAYS_LIMIT)
            if temp_end_date - delta >= start_date:
                partitions.append((temp_end_date.strftime(DATE_FORMAT), (temp_end_date - delta).strftime(DATE_FORMAT)))
                temp_end_date = temp_end_date - delta - timedelta(days=1)
            else:
                partitions.append((temp_end_date.strftime(DATE_FORMAT), start_date.strftime(DATE_FORMAT)))
                break
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
    interpolated = []
    for i in range(len(dates) - 1):
            if dates[i] not in new_dates:
                new_dates.append(dates[i])
                new_rates.append(rates[i])
                interpolated.append(False)
            difference = (datetime.strptime(dates[i + 1], DATE_FORMAT) - datetime.strptime(dates[i], DATE_FORMAT)).days
            if difference > 1:
                for j in range(difference-1):
                    new_dates.append((datetime.strptime(dates[i], DATE_FORMAT) + timedelta(j+1)).strftime(DATE_FORMAT))
                    new_rates.append(rates[i])
                    interpolated.append(True)
            else:
                new_dates.append(dates[i+1])
                new_rates.append(rates[i+1])
                interpolated.append(False)
    if dates[len(dates) - 1] not in new_dates:
        new_rates.append(rates[len(rates) - 1])
        interpolated.append(False)
    begin_diff = (datetime.strptime(dates[0], DATE_FORMAT) - datetime.strptime(partition[1], DATE_FORMAT)).days
    if begin_diff > 0:
        first_date = new_dates[0]
        for i in range(begin_diff):
            new_dates.insert(0, (datetime.strptime(first_date, DATE_FORMAT) - timedelta(i+1)).strftime(DATE_FORMAT))
            new_rates.insert(0, last_rate)
            interpolated.append(True)
    end_diff = (datetime.strptime(partition[0], DATE_FORMAT) - datetime.strptime(new_dates[len(new_dates)-1], DATE_FORMAT)).days
    if end_diff > 0:
        last_date = new_dates[len(new_dates) - 1]
        for i in range(end_diff):
            new_dates.insert(len(new_dates), (datetime.strptime(last_date, DATE_FORMAT) + timedelta(i+1)).strftime(DATE_FORMAT))
            new_rates.insert(len(new_rates), new_rates[len(new_rates)-1])
            interpolated.append(True)
    return (new_dates, new_rates, interpolated)

def fill_exchange_rates_table(data):
    drop_exchange_rates_table()
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
