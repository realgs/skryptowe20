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
                  (date DATE, price real, interpolation integer)
                  ''')
   connection.commit()
   connection.close()

def fillTableWithData():
   connection = sqlite3.connect(databaseFile)
   cursor = connection.cursor()
   cursor.execute('SELECT order_date FROM SalesOrder GROUP BY order_date ORDER BY order_date DESC')
   dates = []
   values = []
   for date in cursor.fetchall():
      dates.append(datetime.datetime.strptime(date[0], '%Y-%m-%d').date())
   for date in dates:
      resp = requests.get(_url(date))
      if resp.status_code != 200:
         if len(values) != 0:
            values.append((date, values[-1][1], 1))
         else:
            previousDate = date
            while(resp.status_code != 200):
                previousDate = previousDate - datetime.timedelta(days=1)
                resp = requests.get(_url(previousDate))
            price = resp.json()['rates'][0]['mid']
            values.append((date, price, 1))
      else:
         price = resp.json()['rates'][0]['mid']
         values.append((date, price, 0))

   cursor.executemany('INSERT INTO CurrencyQuotes VALUES (?,?,?)', values)
   connection.commit()
   connection.close()
