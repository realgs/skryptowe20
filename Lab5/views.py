import json
import sqlite3
import requests
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

dataBase='salesData.db'
rates='rates'
no='no'
mid='mid'
next=1
success=200
l=5
formatDay="%Y-%m-%d"
startDay= '2014-03-18'
endDay='2016-07-11'
tempDay='2015-01-01'
usd='usd'


def makeDate(date):
    thisDate = date.strftime(formatDay)
    return thisDate

def addTableWithInterpolated():
    conn = sqlite3.connect(dataBase)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE AverageCurrencyUSDPLN (Id,DateOfValue,AverageCurrency,Interpolated);''')
    conn.commit()
    dateToTable = {}
    interpol=[]
    endDate = datetime.datetime.strptime(startDay, formatDay)
    todayDate = datetime.datetime.strptime(endDay, formatDay)
    while (todayDate > endDate):
        resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/{}/'.format(makeDate(todayDate)))
        if resp.status_code != success:
            dateToTable[makeDate(todayDate)] = prev_resp.json()[rates][0][mid]
            interpol.append(True)
        else:
            prev_resp = resp
            dateToTable[makeDate(todayDate)] = resp.json()[rates][0][mid]
            interpol.append(False)
        todayDate = todayDate - datetime.timedelta(days=1)
    pos = 0
    for k, v in dateToTable.items():
        pos += 1
        todayDate = datetime.datetime.strptime(k, formatDay)
        conn.execute("INSERT INTO AverageCurrencyUSDPLN (Id,DateOfValue,AverageCurrency,Interpolated) VALUES (?,?,?,?)",
                     (pos, makeDate(todayDate), v,interpol[pos-1]))
    conn.commit()
    conn.close()

def createNewTableSales():
    conn = sqlite3.connect(dataBase)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE SumOfSales (Id,DateOfSale,SalesPLN,SalesUSD);''')
    conn.commit()
    cursor.execute('''SELECT SalesOrder.order_date, SalesOrder.sales, AverageCurrencyUSDPLN.AverageCurrency
                                FROM SalesOrder JOIN AverageCurrencyUSDPLN ON SalesOrder.order_date=AverageCurrencyUSDPLN.DateOfValue''')
    salesUSD = {}
    salesPLN = {}
    for elem in cursor:
        if elem[1] is not None:
            if str(elem[0]) not in salesUSD:
                salesUSD[str(elem[0])] = elem[1]
            else:
                salesUSD[str(elem[0])] += elem[1]
            if str(elem[0]) not in salesPLN:
                salesPLN[str(elem[0])] = elem[1] * elem[2]
            else:
                salesPLN[str(elem[0])] += (elem[1] * elem[2])

    pos=0
    for k,v in salesPLN.items():
        pos+=1
        conn.execute("INSERT INTO SumOfSales (Id,DateOfSale,SalesPLN,SalesUSD) VALUES (?,?,?,?)",
                     (pos, k, v, salesUSD[k]))
    conn.commit()
    conn.close()

class TestView(APIView):

    def exchangeRates(self,date):
        rateFromDate = {}
        conn = sqlite3.connect(dataBase)
        cursor = conn.cursor()
        cursor.execute('''SELECT Id,DateOfValue,AverageCurrency,Interpolated
                            FROM AverageCurrencyUSDPLN''')
        for elem in cursor:
            if elem[1] == date:
                rateFromDate['Id']=elem[0]
                rateFromDate['Date']=date
                rateFromDate['Rate of USD']=elem[2]
                if elem[3] == 1: rateFromDate['Interpolated'] = True
                else: rateFromDate['Interpolated'] = False

        return rateFromDate

    def sales(self, date):
        sales = {}
        conn = sqlite3.connect(dataBase)
        cursor = conn.cursor()
        cursor.execute('''SELECT Id,DateOfSale,SalesPLN,SalesUSD
                                    FROM SumOfSales''')
        for elem in cursor:
            if elem[1] == date:
                sales['Id'] = elem[0]
                sales['Date'] = date
                sales['Sales in PLN'] = elem[2]
                sales['Sales in USD'] = elem[3]
        conn.close()
        return sales

    def get(self, request, oper=usd, date=tempDay):
        if datetime.datetime.strptime(date, formatDay) > datetime.datetime.strptime(endDay,
                                                                                    formatDay) or datetime.datetime.strptime(
                date, formatDay) < datetime.datetime.strptime(startDay, formatDay):
            data = {'Data spoza przedziału zawartego w bazie': date}
        else:
            if(oper == 'sales'):
                data = self.sales(date)
                if data == None or data == {}: data = {'Brak sprzedaży w dniu': date}
            elif(oper == usd):
                data = self.exchangeRates(date)
                if data == None or data == {}: data = {'Zła data kursu': date}
            else: data = {'Zły format':'wpisz /usd albo /sales'}
        return Response(data)
