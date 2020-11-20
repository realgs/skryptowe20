import data
import matplotlib.pyplot as plt
import pandas as pd


def plot_2_currencies(curr1_data, curr2_data):
    fig, ax = plt.subplots(figsize=(20, 10))
    curr1_data = pd.DataFrame(curr1_data)
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


def plot():
    curr1 = 'usd'
    curr2 = 'eur'
    days = 180
    usd_data = data.get_currency_last_x_days(currency=curr1, days=days)
    eur_data = data.get_currency_last_x_days(currency=curr2, days=days)

    plot_2_currencies(usd_data, eur_data)


plot()
