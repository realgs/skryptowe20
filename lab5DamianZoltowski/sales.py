import sqlite3
from salesDataObject import SalesDataObject

class Sales:

    def __init__(self):
        self.salesArray = []

    def calculateSales(self):
        connection = sqlite3.connect('sales_data_base.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT order_date, SUM(sales), SUM(sales) * price 
                          FROM SalesOrder JOIN CurrencyQuotes ON order_date = date 
                          GROUP BY order_date 
                          ORDER BY order_date DESC
                          ''')
        for order in cursor.fetchall():
            dataObject = SalesDataObject(order[0], order[1], order[2])
            self.salesArray.append(dataObject)
        connection.close()

    def findSales(self, date):
        for sale in self.salesArray:
            if sale.date == date:
                return sale
        return None
