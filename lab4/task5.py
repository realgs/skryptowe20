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
                      WHERE date BETWEEN '2013-01-01' AND '2015-12-31'
                      GROUP BY date
                      ORDER BY date''')
    for date in cursor.fetchall():
        dates.append(datetime.datetime.strptime(date[0], '%Y-%m-%d').date())
    cursor.execute('''SELECT order_date, SUM(sales), price
                      FROM SalesOrder JOIN CurrencyQuotes ON order_date = date
                      WHERE order_date BETWEEN '2013-01-01' AND '2015-12-31'
                      GROUP BY order_date
                      ORDER BY 1''')
    for data in cursor.fetchall():
        USDSales.append(data[1])
        PLNSales.append(data[2] * data[1])

    plt.plot(dates, USDSales, color='red', label='USD SALES', linestyle='-')
    plt.plot(dates, PLNSales, color='blue', label='PLN SALES',  linestyle='-')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Sales Value', fontsize=14)
    plt.legend()
    plt.title("PLN and USD total sales values during years 2013-2015")
    plt.savefig('task5.svg')
    plt.show()
    connection.close()

drawSalesChart()