import sys
import django
django.setup()

from os import path
from api_exchange.models import ExchangeRate
sys.path.append(path.abspath('../lab4'))
import manage_db
import plot_data


def merge_tables(currency_data, transaction_data):
    transact_iter = 0
    iter2 = 0
    for currency_row in currency_data:
        iter2 += 1
        vol_pln = 0
        vol_usd = 0
        while currency_row['effectiveDate'] == transaction_data[0][transact_iter] and \
                transact_iter < len(transaction_data[0]) - 1:
            vol_pln += transaction_data[2][transact_iter]
            vol_usd += transaction_data[1][transact_iter]
            transact_iter += 1
        currency_row['volume_pln'] = vol_pln
        currency_row['volume_usd'] = vol_usd
    print(*currency_data, sep='\n')
    return currency_data


def get_data():
    currency_data = manage_db.data.get_currency_from_period('usd', date_from='2004-05-05', date_to='2005-05-07')
    currency_data = manage_db.add_weekend_rates(currency_data)
    transactions = plot_data.get_plot_data()
    return currency_data, transactions


def insert_data_to_db():
    currency_data, transaction_data = get_data()
    merge_tables(currency_data, transaction_data)
    currency_data_merged = merge_tables(currency_data, transaction_data)
    for row in currency_data_merged:
        a = ExchangeRate(date=row['effectiveDate'],
                         rate=row['mid'],
                         interpolated=row['interpolated'],
                         volumePLN=row['volume_pln'],
                         volumeUSD=row['volume_usd'])
        a.save()


if __name__ == '__main__':
    insert_data_to_db()
