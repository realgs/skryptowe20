import data
import query_db as db
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


def plot_2_currencies(curr1_data, curr2_data):
    fig, ax = plt.subplots(figsize=(20, 10))
    curr1_data = pd.DataFrame(curr1_data)
    print(curr1_data)
    curr2_data = pd.DataFrame(curr2_data)
    ax.xaxis.set_major_locator(plt.MaxNLocator(51))
    plt.xticks(rotation=90)
    ax.plot(curr1_data['effectiveDate'], curr1_data['mid'], color='blue', label='USD [$]')
    ax.plot(curr2_data['effectiveDate'], curr2_data['mid'], color='green', label='EURO [€]')
    plt.legend()
    plt.title('USD, EURO to PLN in 180 days', fontsize=20)
    ax.set_xlabel('DATE', fontsize=16)
    ax.set_ylabel("PLN", fontsize=16)
    plt.show()
    fig.savefig('usd_euro_to_pln_chart.svg', format='svg', dpi=200, bbox_inches='tight')


def plot_transactions(plot_data):
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(51))
    plt.xticks(rotation=90)
    ax.plot(plot_data[0], plot_data[1], color="blue", label='USD [$]', marker='o')
    ax2 = ax.twinx()
    ax2.plot(plot_data[0], plot_data[2], color="red", label="PLN", marker='o')
    plt.title('TRANSACTIONS BY DATE IN USD AND PLN', fontsize=20)
    ax.set_xlabel('DATE', fontsize=16)
    ax.set_ylabel("USD", fontsize=16)
    ax2.set_ylabel('PLN', fontsize=16)
    plt.show()
    fig.savefig('transactions.svg', format='svg', dpi=200, bbox_inches='tight')


def prepare_data(transaction_logs, currency_rates):
    transactions = []
    rates = []
    for log in transaction_logs:
        tmp = (datetime.strftime(log.order_date, "%Y-%m-%d"), log.sales)
        transactions.append(tmp)
    for rate in currency_rates:
        tmp = (datetime.strftime(rate.date, "%Y-%m-%d"), rate.rate)
        rates.append(tmp)

    rates_dates = []
    for date in rates:
        rates_dates.append(date[0])

    plot_data = []
    for transaction in transactions:
        try:
            index = rates_dates.index(transaction[0])
            date = transaction[0]
            usd_val = transaction[1]
            pln_val = transaction[1] * rates[index][1]
            row = (date, usd_val, pln_val)
            plot_data.append(row)
        except ValueError:
            "Date not found"

    df = pd.DataFrame(plot_data)
    return df


def plot():
    curr1 = 'usd'
    curr2 = 'eur'
    days = 180
    usd_data = data.get_currency_last_x_days(currency=curr1, days=days)
    eur_data = data.get_currency_last_x_days(currency=curr2, days=days)
    transaction_logs = db.get_transaction_logs()
    currency_rates = db.get_currency_rates()

    plot_2_currencies(usd_data, eur_data)
    plot_data = prepare_data(transaction_logs, currency_rates)
    plot_transactions(plot_data)
