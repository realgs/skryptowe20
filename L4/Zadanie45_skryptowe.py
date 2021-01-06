import sqlite3
import datetime
import requests
import json
import numpy as np
import matplotlib.pyplot as plt

def CreateNewTable():
    conn=sqlite3.connect('salesData.db')
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE AverageCurrencyUSDPLN (Id,DateOfValue,AverageCurrency);''' )
    conn.commit()
    dateToTable={}
    endDate=datetime.datetime.strptime('2014-03-18','%Y-%m-%d')
    todayDate=datetime.datetime.strptime('2016-07-11','%Y-%m-%d')
    while(todayDate>endDate):
        resp=requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/{}/'.format(makeDate(todayDate))) 
        if resp.status_code !=200: dateToTable[makeDate(todayDate)] = prev_resp.json()['rates'][0]['mid']
        else:
            prev_resp = resp
            dateToTable[makeDate(todayDate)]=resp.json()['rates'][0]['mid']
        todayDate=todayDate-datetime.timedelta(days=1)
    pos=0
    for k,v in dateToTable.items():
        pos+=1
        todayDate=datetime.datetime.strptime(k,'%Y-%m-%d')
        conn.execute("INSERT INTO AverageCurrencyUSDPLN (Id,DateOfValue,AverageCurrency) VALUES (?,?,?)",(pos, makeDate(todayDate),v))
    conn.commit()
    conn.close()

def makeDate(date):
    thisDate=date.strftime("%Y-%m-%d")
    return thisDate
    
def SalesChartUSDPLN():
    conn=sqlite3.connect('salesData.db')
    cursor=conn.cursor()
    cursor.execute('''SELECT SalesOrder.order_date, SalesOrder.sales, AverageCurrencyUSDPLN.AverageCurrency
                    FROM SalesOrder JOIN AverageCurrencyUSDPLN ON SalesOrder.order_date=AverageCurrencyUSDPLN.DateOfValue''')
    salesUSD={}
    salesPLN={}
    for elem in cursor:
        if elem[1] is not None:
            if str(elem[0]) not in salesUSD: salesUSD[str(elem[0])]=elem[1]
            else: salesUSD[str(elem[0])]+=elem[1]
            if str(elem[0]) not in salesPLN: salesPLN[str(elem[0])]=elem[1]*elem[2]
            else: salesPLN[str(elem[0])]+=(elem[1]*elem[2])
    CreateChartUSDPLN(salesUSD,salesPLN)

def CreateChartUSDPLN(salU,salP):
    xUSD=[]
    yUSD=[]
    xPLN=[]
    yPLN=[]
    (xUSD,yUSD)=FromDictToTabs(salU,xUSD,yUSD)
    (xPLN,yPLN)=FromDictToTabs(salP,xPLN,yPLN)
    plt.plot(xUSD[::-1],yUSD[::-1])
    plt.plot(xPLN[::-1],yPLN[::-1])
    xUSDShort=xUSD[::-30]
    plt.xticks(range(0,len(xUSD),30),xUSDShort)
    plt.xlabel('Dates')
    plt.ylabel('Sales values')
    plt.title('Comparision of sales in USD and PLN')
    plt.legend(['Sales in USD','Sales in PLN'])
    plt.grid(True)
    plt.gcf().autofmt_xdate(rotation=25)
    plt.savefig("Sales.svg")
    plt.show()

def FromDictToTabs(sales,x,y):
    for k,v in sales.items():
        x.append(k)
        y.append(v)
    return (x,y)

if __name__=='__main__':
    #CreateNewTable()
    SalesChartUSDPLN()
    