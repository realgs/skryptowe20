import sqlite3 as sql
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import config


def draw_plot(x_ax, usd, pln, dates_counter):
    plt.plot(x_ax, usd, label='PLN', color='C0')
    plt.plot(x_ax, pln, label='USD', color='C1')
    patches = [mpatches.Patch(label='PLN earnings', color='C0'),
               mpatches.Patch(label='USD earnings', color='C1')]
    plt.legend(handles=patches)
    shown_values = [dates[i] for i in range(0, len(dates), int(len(dates) / dates_counter))]
    plt.title("Earnings in USD and PLN")
    plt.xlabel("Dates")
    plt.ylabel("Earnings")
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.xticks(shown_values, horizontalalignment='center')
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: '%1.fK' % (x * 1e-3)))
    plt.ylim(0)
    plt.xlim(x_ax[0], x_ax[-1])
    plt.grid(True)
    return plt


def fetch_sql_data():
    orders_exec = '''SELECT order_date, 
       Sum(DISTINCT sales*quantity) "USD price", 
       rate, 
       Sum(DISTINCT sales*quantity)/ rate "PLN rate"
       FROM SalesOrder
            JOIN CurrencyData ON rating_date=order_date
       GROUP BY order_date;'''

    c = sql.connect(config.DATABASE_FILENAME)
    cursor = c.cursor()
    cursor.execute(orders_exec)

    return cursor.fetchall()


if __name__ == '__main__':
    rows = fetch_sql_data()
    dates = []
    sum_usd = 0
    usd_sum = []
    sum_pln = 0
    pln_sum = []
    for order_date, usd_price, _, pln_price in rows:
        dates.append(order_date)
        usd_sum.append(usd_price)
        pln_sum.append(pln_price)

    plot = draw_plot(dates, usd_sum, pln_sum, 12)
    plot.savefig("Sum_of_sales.svg")
    plot.show()
