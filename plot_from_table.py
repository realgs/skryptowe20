import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def __plot_chart(sums_usd, sums_pln, days):
    plt.title('Łączna sprzedaż w USD i PLN')
    plt.ylabel('Kwota')
    plt.xlabel('Data')

    plt.scatter(days, sums_usd, color='green', marker='.', label='USD')
    plt.scatter(days, sums_pln, color='red', marker='.', label='PLN')
    plt.legend()

    current_axes = plt.gca()
    plt.xticks(rotation=270)
    current_axes.xaxis.set_major_locator(MultipleLocator(30))
    current_axes.xaxis.set_minor_locator(MultipleLocator(5))

    current_axes.yaxis.set_major_locator(MultipleLocator(10))
    current_axes.yaxis.set_minor_locator(MultipleLocator(2.5))
    plt.show()


def __process_data(transactions, exchange_rates):
    sums_usd = []
    sums_pln = []
    transaction_date = transactions[0][0].replace(' 00:00:00', '')
    transaction_index = 1
    for (date, rate) in exchange_rates:
        sum = 0
        while transaction_index < len(transactions) and transaction_date == date:
            sum += transactions[transaction_index][1]
            transaction_index += 1
            if transaction_index < len(transactions):
                transaction_date = transactions[transaction_index][0].replace(' 00:00:00', '')
        sums_usd.append(sum)
        sums_pln.append(sum * rate)
    dates = [t[0] for t in exchange_rates]
    __plot_chart(sums_usd, sums_pln, dates)


def __main():
    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    c.execute("SELECT InvoiceDate, Total FROM invoices WHERE InvoiceDate BETWEEN '2009-01-01' AND '2010-12-31'")
    transactions = c.fetchall()
    c.execute('SELECT * FROM exchange_rate')
    exchange_rates = c.fetchall()
    conn.commit()
    conn.close()

    __process_data(transactions, exchange_rates)


if __name__ == '__main__':
    __main()
