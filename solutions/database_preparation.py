import datetime
import matplotlib.pyplot as plt
from pymongo import MongoClient
from api_usage import get_currency_quotes

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
    interpolated = False

    if str(dates[0].date()) in dollar_rates.keys():
        last_ratio = dates[0]
    else:
        last_ratio = list(get_currency_quotes('USD', start_date.date() - datetime.timedelta(weeks=1),
                                              start_date.date()).values())[-1]
    for date in dates:
        if str(date.date()) in dollar_rates.keys():
            last_ratio = dollar_rates[str(date.date())]
            interpolated = False
        else:
            interpolated = True

        collection.insert_one({'date': date, 'pln_to_usd': last_ratio, 'interpolated': interpolated})


def create_transaction_summary_collection(days, start_date):
    client = MongoClient()
    db = client[DB_NAME]
    db.drop_collection('transaction_summary')
    db.create_collection('transaction_summary')
    sales_collection = db.sales
    transaction_collection = db.transaction_summary
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

    for data in transactions_data:
        year, month, day = data['_id'].values()
        date = datetime.datetime(year, month, day)
        transactions_sum = float(data['transactions_sum'].to_decimal())

        transaction_collection.insert_one({'date': date, 
        'pln': transactions_sum * pln_exchange_rates_collection.find_one({'date': date})['pln_to_usd'], 
        'usd': transactions_sum})


if __name__ == '__main__':
    start_date = datetime.datetime(2014, 1, 1, 0, 0, 0, 0)
    create_pln_usd_exchange_collection(730, start_date)
    create_transaction_summary_collection(365, start_date)