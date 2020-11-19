import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sqlite3
import datetime

databaseFile = 'sales_data_base.db'


def drawSalesChart():
    connection = sqlite3.connect(databaseFile)
    cursor = connection.cursor()
    dates = []
    USDSales = []
    PLNSales = []
    cursor.execute('''SELECT date 
                      FROM CurrencyQuotes 
                      GROUP BY date
                      ORDER BY date''')
    for date in cursor.fetchall():
        date = datetime.datetime.strptime(date[0], '%Y-%m-%d').strftime('%Y-%m')
        dates.append(date)
    cursor.execute('''SELECT order_date, SUM(sales), price
                      FROM SalesOrder JOIN CurrencyQuotes ON order_date = date                 
                      GROUP BY order_date
                      ORDER BY 1''')
    for data in cursor.fetchall():
        USDSales.append(data[1])
        PLNSales.append(data[2] * data[1])

    plt.plot([], [], color='red', label='USD SALES', linewidth=3)
    plt.plot([], [], color='blue', label='PLN SALES', linewidth=3)
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(20000))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(2000))
    plt.stackplot(dates, USDSales, PLNSales, colors=['r', 'b'])
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Sales Value', fontsize=14)
    plt.legend()
    plt.title("PLN and USD total sales values during years 2013-2016")
    plt.savefig('task5.svg')
    plt.show()
    connection.close()


