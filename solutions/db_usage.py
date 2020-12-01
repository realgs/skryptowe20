"""Dane pochodza z https://github.com/huynhsamha/quick-mongo-atlas-datasets"""

import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient
from api_usage import get_currency_quotes

sns.set()

FIGSIZE = (12, 6)
DB_NAME = 'sample_supplies'


def create_pln_usd_exchange_collection(days, start_date):
    client = MongoClient()
    db = client[DB_NAME]
    db.drop_collection('PLN_exchange_rates')
    db.create_collection('PLN_exchange_rates')
    collection = db.PLN_exchange_rates

    end_date = start_date + datetime.timedelta(days=days)
    dates = [start_date + datetime.timedelta(days=x) for x in range(days)]
    dollar_rates = get_currency_quotes('USD', start_date.date(), end_date.date())
    if dates[0] in dollar_rates:
        last_ratio = dates[0]
    else:
        last_ratio = list(get_currency_quotes('USD', start_date.date() - datetime.timedelta(weeks=1),
                                              start_date.date()).values())[-1]
    for date in dates:
        if date in dollar_rates:
            last_ratio = dollar_rates[date]
        collection.insert_one({'date': date, 'pln_to_usd': last_ratio})


def create_usd_pln_plot(days, start_date):
    client = MongoClient()
    db = client[DB_NAME]
    sales_collection = db.sales
    pln_exchange_rates_collection = db.PLN_exchange_rates

    end_date = start_date + datetime.timedelta(days=days)

    transactions_data = sales_collection.aggregate([
        {'$match': {
            'saleDate': {'$gte': start_date, '$lte': end_date}}},
        {'$project': {
            'day': {"$dayOfMonth": "$saleDate"},
            'month': {"$month": "$saleDate"},
            'year': {"$year": "$saleDate"},
            'item': '$items'
        }},
        {'$unwind': '$item'},
        {'$project': {
            'day': "$day",
            'month': "$month",
            'year': "$year",
            'price': '$item.price'
        }},
        {'$group': {
            '_id': {'year': "$year", 'month': "$month", 'day': "$day"},
            'transactions_sum': {"$sum": '$price'}
        }},
        {'$sort': {
            '_id': 1
        }}
    ])

    dates, usd_transactions_sum, pln_transactions_sum = [], [], []
    for data in transactions_data:
        year, month, day = data['_id'].values()
        date = datetime.datetime(year, month, day)
        transactions_sum = float(data['transactions_sum'].to_decimal())
        dates.append(date)
        usd_transactions_sum.append(transactions_sum)
        pln_transactions_sum.append(
            transactions_sum * pln_exchange_rates_collection.find_one({'date': date})['pln_to_usd'])

    plt.figure(figsize=FIGSIZE)
    plt.plot(dates, usd_transactions_sum, color='green', label='USD', linewidth=1)
    plt.plot(dates, pln_transactions_sum, color='red', label='PLN', linewidth=1)
    plt.title('Łączna wartość transakcji ze zbioru MongoDB Atlas Supply Store w dniach 2014-01-01 - 2014-12-31 w PLN i USD')
    plt.xlabel('Data')
    plt.ylabel('Łączna wartość transakcji')
    plt.legend()
    plt.xticks(dates[::20], rotation=25)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig('transactions_sum.svg', format='svg')
    plt.show()


if __name__ == '__main__':
    start_date = datetime.datetime(2014, 1, 1, 0, 0, 0, 0)
    create_pln_usd_exchange_collection(730, start_date)
    create_usd_pln_plot(365, start_date)
