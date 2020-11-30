import sqlite3
import datetime
import requests

databaseFile = 'sales_data_base.db'

def _url(date):
   return 'http://api.nbp.pl/api/exchangerates/rates/A/USD/' + datetime.date.strftime(date, '%Y-%m-%d')

def createTableCurrencyQuotes():
   connection = sqlite3.connect(databaseFile)
   cursor = connection.cursor()
   cursor.execute('''
                  CREATE TABLE CurrencyQuotes   
                  (date text, price real)
                  ''')
   connection.commit()
   connection.close()

def fillTableWithData():
   connection = sqlite3.connect(databaseFile)
   cursor = connection.cursor()
   cursor.execute('SELECT order_date FROM SalesOrder ORDER BY order_date DESC')
   dates = []
   prices = []
   for date in cursor.fetchall():
      dates.append(datetime.datetime.strptime(date[0], '%Y-%m-%d').date())
   for date in dates:
      resp = requests.get(_url(date))
      if resp.status_code != 200:
         previousDate = date
         while(resp.status_code != 200):
            previousDate = previousDate - datetime.timedelta(days=1)
            resp = requests.get(_url(previousDate))
         prices.append(resp.json()['rates'][0]['mid'])
      else:
         prices.append(resp.json()['rates'][0]['mid'])
   USDPrices = []
   for i in range(0, len(dates)):
      queryData = (dates[i], prices[i])
      USDPrices.append(queryData)

   cursor.executemany('INSERT INTO CurrencyQuotes VALUES (?,?)', USDPrices)
   connection.commit()
   connection.close()
