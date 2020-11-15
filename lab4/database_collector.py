import pyodbc
import sqlite3 as sql
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

if __name__ == '__main__':
    dates_counter = 5
    orders_exec = '''SELECT order_date, 
    Sum(DISTINCT sales) "USD price", 
    rate, 
    Sum(DISTINCT sales)/ rate "PLN rate"
    FROM SalesOrder
         JOIN CurrencyData
    WHERE order_date = rating_date
    GROUP BY order_date;'''

    c = sql.connect('salesData.db')
    cursor = c.cursor()
    cursor.execute(orders_exec)

    rows = cursor.fetchall()
    dates = []
    sum_usd = 0
    usd_sum = []
    sum_pln = 0
    pln_sum = []
    for order_date, usd_price, _, pln_price in rows:
        dates.append(order_date)
        sum_usd = sum_usd + usd_price
        usd_sum.append(sum_usd)
        sum_pln = sum_pln + pln_price
        pln_sum.append(sum_pln)

    plt.plot(dates, usd_sum, label='PLN', color='C0')
    plt.plot(dates, pln_sum, label='USD', color='C1')
    patches = [mpatches.Patch(label='PLN earnings', color='C0'),
               mpatches.Patch(label='USD earnings', color='C1')]
    plt.legend(handles=patches)
    shown_values = [dates[i] for i in range(0, len(dates), int(len(dates) / dates_counter))]
    plt.title("Earnings in USD and PLN")
    plt.xlabel("Dates of sales")
    plt.ylabel("Earnings")
    plt.xticks(shown_values, horizontalalignment='center')
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: '%1.fK' % (x * 1e-2)))
    plt.ylim(0)
    plt.xlim(0)
    plt.grid(True)
    plt.savefig('Sum_of_sales.svg')
    plt.show()
