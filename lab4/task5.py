import matplotlib.pyplot as plt
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
        dates.append(datetime.datetime.strptime(date[0], '%Y-%m-%d').date())
    cursor.execute('''SELECT order_date, SUM(sales), SUM(price)
                      FROM SalesOrder JOIN CurrencyQuotes ON order_date = date
                      GROUP BY order_date
                      ORDER BY 1''')
    for date in cursor.fetchall():
        USDSales.append(date[1])
        PLNSales.append(date[2])

    plt.plot(dates, USDSales, color='red', label='USD SALES')
    plt.plot(dates, PLNSales, color='blue', label='PLN SALES')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Sales Value', fontsize=14)
    plt.legend()
    plt.title("PLN and USD total sales values during years 2013-2016")
    plt.show()
    plt.savefig('task5.svg')
    connection.close()

