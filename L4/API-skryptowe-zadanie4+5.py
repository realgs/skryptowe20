import sqlite3
import datetime 
import requests
import json
import numpy as np
import matplotlib.pyplot as plt

def addTable():
    conn = sqlite3.connect('salesData.db')
    cursor = conn.cursor()
    print("Database file - connected")

    cursor.execute('''CREATE TABLE USDPLNAverangeCur (Id, DateValue, AverageCurrency); ''')
    conn.commit()

    resultDays = {}
    lastDate = datetime.datetime.strptime('2014-08-18', '%Y-%m-%d')
    dateNow= datetime.datetime.strptime('2016-11-04', '%Y-%m-%d')

    while(dateNow>lastDate):
        resp=requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/{dateNow}/'.format(dateNow=dateNow.strftime("%Y-%m-%d")))
        if resp.status_code != 200:
            resultDays[dateNow.strftime('%Y-%m-%d')]=prevResp.json()['rates'][0]['mid']
        else:
            prevResp=resp
            resultDays[dateNow.strftime('%Y-%m-%d')]=resp.json()['rates'][0]['mid']
        dateNow=dateNow-datetime.timedelta(days=1)
    position = 0
    for key, value in resultDays.items():
        position+=1
        dateNow = datetime.datetime.strptime(key, '%Y-%m-%d')
        conn.execute("INSERT INTO USDPLNAverangeCur (Id, DateValue, AverageCurrency)\
            VALUES(?,?,?)",(position, dateNow.strftime('%Y-%m-%d'), value))
        
    conn.commit()
    conn.close()

def createDiagram():
    conn=sqlite3.connect('salesData.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT SalesOrder.order_date, SalesOrder.sales, USDPLNAverangeCur.AverageCurrency
                        FROM SalesOrder JOIN USDPLNAverangeCur ON SalesOrder.order_date = USDPLNAverangeCur.DateValue''')
                        
    plnSales = {}
    usdSales = {}

    for element in cursor:
        if element[1] is not None:
            if str(element[0]) not in usdSales:
                usdSales[str(element[0])]=element[1]
            else:
                usdSales[str(element[0])]+=element[1]

            if str(element[0]) not in plnSales:
                plnSales[str(element[0])]=(element[1]*element[2])
            else:
                plnSales[str(element[0])]+=(element[1] *element[2])

    SalesChart(usdSales, plnSales)

def SalesChart(usdSale, plnSale):
    usd_dates = []
    usd_rates = []
    pln_dates = []
    pln_rates = []

    for key, value in usdSale.items():
        usd_dates.append(key)
        usd_rates.append(value)

    for key, value in plnSale.items():
        pln_dates.append(key)
        pln_rates.append(value)

    plt.plot(usd_dates, usd_rates)
    plt.plot(pln_dates, pln_rates)
    plt.title('Wykres sprzedaży')
    plt.xlabel('Daty sprzedaży')
    plt.ylabel('Wartości sprzedaży')
    plt.legend(['Wartości w dolarach', 'Wartości w złotych'])
    plt.grid(True)
    plt.savefig("USD_PLN_SALES_Chart")
    plt.show()
    
if __name__=='__main__':
    #addTable()
    createDiagram()