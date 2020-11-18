import matplotlib.pyplot as plt
from currency_rates import get_rete_of_currency
from database import get_transactions_usd_and_pln


def generate_plot_usd_eur(days):
    usd = get_rete_of_currency('usd', days)
    eur = get_rete_of_currency('eur', days)

    usd_time = [u['effectiveDate'] for u in usd['rates']]
    usd_value = [u['mid'] for u in usd['rates']]

    euro_time = [e['effectiveDate'] for e in eur['rates']]
    euro_value = [e['mid'] for e in eur['rates']]

    fig, ax = plt.subplots()

    ax.plot(usd_time, usd_value, label='usd')
    ax.plot(euro_time, euro_value, label='euro')
    ax.set_xticks(ax.get_xticks()[::len(ax.get_xticks()) // 4])
    plt.xlabel('Czas', fontsize=14)
    plt.ylabel('Cena [PLN]', fontsize=14)
    plt.legend(loc='upper left')
    plt.show()

def plot_database(begin, end):
    sales = get_transactions_usd_and_pln(begin, end)
    time = [sale[0] for sale in sales]
    usd = [sale[1] for sale in sales]
    pln = [sale[2] for sale in sales]
    fig, ax = plt.subplots()

    ax.plot(time, usd, label='usd')
    ax.plot(time, pln, label='pln')
    ax.set_xticks(ax.get_xticks()[::len(ax.get_xticks()) // 4])
    plt.xlabel('Czas', fontsize=14)
    plt.ylabel('Dzienna sprzedaż', fontsize=14)
    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    generate_plot_usd_eur(360)
    plot_database('2007-06-05', '2007-11-20')