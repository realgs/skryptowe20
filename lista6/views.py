import sqlite3
import requests
import json
import datetime
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from django.shortcuts import render
# Create your views here.
l = 5
salesData = 'salesData.db'
text = "Wrong value"
format = "%Y-%m-%d"
datefist = '2015-01-01'
currfirst = 'usd'

class TestView(APIView):

    def dataRates(self, days):
        rates = {}
        conn = sqlite3.connect('salesData.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT Id, DateValue, AverageCurrency, Interpolated
                                FROM USDPLNAverangeCur''')
        for elem in cursor:
            if elem[1] == days:
                rates['Id'] = elem[0]
                rates['Date'] = elem[1]
                rates['USD rate'] = elem[2]
                if elem[3] == 1:
                    rates['Interpolated'] = False
                else:
                    rates['Interpolated'] = True

        return rates

    def valuesSales(self, data):

        conn = sqlite3.connect('salesData.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT Id, Date, SalesPLN, SalesUSD
                                        FROM SalesCount''')
        sales = {}
        for elem in cursor:
            if elem[1] == data:
                sales['Id'] = elem[0]
                sales['Date'] = elem[1]
                sales['PLN'] = elem[2]
                sales['USD'] = elem[3]
        conn.close()
        return sales

    def chartRates(self, datefirst, datesecond):
        dataandrates=[]
        valuerates=[]
        conn = sqlite3.connect('salesData.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT Id, DateValue, AverageCurrency
                                        FROM USDPLNAverangeCur''')
        for elem in cursor:
            if datetime.datetime.strptime(elem[1], format) >= datetime.datetime.strptime(datefirst, format) and datetime.datetime.strptime(elem[1], format) <= datetime.datetime.strptime(datesecond, format):
                dataandrates.append(elem[1])
                valuerates.append(elem[2])
        conn.close()
        return (dataandrates,valuerates)

    def saleschart(self, datefirst, datesecond):
        conn = sqlite3.connect('salesData.db')
        cursor = conn.cursor()
        pln=[]
        usd=[]
        date=[]
        cursor.execute('''SELECT Id, Date, SalesPLN, SalesUSD
                                                FROM SalesCount''')
        for elem in cursor:
            if datetime.datetime.strptime(elem[1], format) >= datetime.datetime.strptime(datefirst, format) and datetime.datetime.strptime(elem[1], format) <= datetime.datetime.strptime(datesecond, format):
                date.append(elem[1])
                pln.append(elem[2])
                usd.append(elem[3])
        return (date, pln, usd)

    def get(self, request, *args, **kwargs):
        date1 = request.GET.get('dateusd')
        data2 = request.GET.get('salesdata')
        datafirst = request.GET.get('datafirst')
        datasecond = request.GET.get('datasecond')
        datafirst2 = request.GET.get('datafirst2')
        datasecond2 = request.GET.get('datasecond2')
        startandend=[]
        value = []
        pln = []
        usd = []
        date = []
        if(datafirst!=None and datasecond!= None):
            (startandend, value)= self.chartRates(datafirst, datasecond)
            if len(startandend) != 0:
                startandend.reverse()
                value.reverse()
                plt.plot(startandend, value)
                if (len(startandend) > 20):
                    dateShort = startandend[::20]
                    plt.xticks(range(0, len(startandend), 20), dateShort)
                plt.title("USD chart")
                plt.xlabel('Dates')
                plt.ylabel('Rates')
                plt.gcf().autofmt_xdate(rotation=25)
                plt.savefig('C:\\Users\\1999a\\PycharmProjects\\lista5skryptoweApi\\lista5skryptowe\\static\\images\\chartRate2.png')
                plt.close()
            else:
                msg = {"Message": "Wrong value"}
                return render (request, "homepage.html", msg)
        if (datafirst2!= None and datasecond2 != None):
            (date, pln, usd) = self.saleschart(datafirst2, datasecond2)
            if len(date) != 0:
                date.reverse()
                pln.reverse()
                usd.reverse()
                plt.plot(date, pln)
                plt.plot(date, usd)
                if(len(date)>20):
                    dateShorter = date[::20]
                    plt.xticks(range(0, len(date), 20), dateShorter)
                plt.title("Sales chart")
                plt.xlabel("Dates")
                plt.ylabel("Sales")
                plt.gcf().autofmt_xdate(rotation=25)
                plt.savefig('C:\\Users\\1999a\\PycharmProjects\\lista5skryptoweApi\\lista5skryptowe\\static\\images\\chartsales2.png')
                plt.close()
            else:
                msg2 = {"Message": "Wrong value"}
                return render(request, "homepage.html", msg2)

        dataUSD = self.dataRates(date1)
        datasales = self.valuesSales(data2)


        if dataUSD.get('Id') != None:
            dataUSD2 = {}
            dataUSD2['Id'] = dataUSD.get('Id')
            dataUSD2['Date'] = dataUSD.get('Date')
            dataUSD2['Rate'] = dataUSD.get('USD rate')
            dataUSD2['Interpolated'] = dataUSD.get('Interpolated')
            return render(request, "homepage.html", dataUSD2)

        if datasales.get('Id') != None:
            dataSales = {}
            dataSales['Id2'] = datasales.get('Id')
            dataSales['Date2'] = datasales.get('Date')
            dataSales['Rate2'] = datasales.get('PLN')
            dataSales['Interpolated2'] = datasales.get('USD')
            return render(request, "homepage.html", dataSales)

        return render(request, "homepage.html")

def addinterpolated():
    conn = sqlite3.connect(salesData)
    cursor = conn.cursor()
    print("Database file - connected")

    cursor.execute('''CREATE TABLE USDPLNAverangeCur (Id, DateValue, AverageCurrency, Interpolated); ''')
    conn.commit()

    resultDays = {}
    lastDate = datetime.datetime.strptime('2014-08-18', '%Y-%m-%d')
    dateNow = datetime.datetime.strptime('2016-11-04', '%Y-%m-%d')
    interpolTable = []
    while (dateNow > lastDate):
        resp = requests.get(
            'http://api.nbp.pl/api/exchangerates/rates/a/usd/{dateNow}/'.format(
                dateNow=dateNow.strftime(format)))
        if resp.status_code != 200:
            resultDays[dateNow.strftime(format)] = prevResp.json()['rates'][0]['mid']
            interpolTable.append(True)
        else:
            prevResp = resp
            resultDays[dateNow.strftime(format)] = resp.json()['rates'][0]['mid']
            interpolTable.append(False)
        dateNow = dateNow - datetime.timedelta(days=1)
    position = 0
    for key, value in resultDays.items():
        position += 1
        dateNow = datetime.datetime.strptime(key, format)
        conn.execute("INSERT INTO USDPLNAverangeCur (Id, DateValue, AverageCurrency, Interpolated)\
                VALUES(?,?,?,?)", (position, dateNow.strftime(format), value, interpolTable[position - 1]))

    conn.commit()
    conn.close()
def createSalesTable():
    conn = sqlite3.connect(salesData)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE SalesCount (Id, Date, SalesPLN, SalesUSD); ''')
    conn.commit()

    cursor.execute('''SELECT SalesOrder.order_date, SalesOrder.sales, USDPLNAverangeCur.AverageCurrency
                                    FROM SalesOrder JOIN USDPLNAverangeCur ON SalesOrder.order_date = USDPLNAverangeCur.DateValue''')
    plnSales = {}
    usdSales = {}

    for element in cursor:
        if element[1] is not None:
            if str(element[0]) not in usdSales:
                usdSales[str(element[0])] = element[1]
            else:
                usdSales[str(element[0])] += element[1]

            if str(element[0]) not in plnSales:
                plnSales[str(element[0])] = (element[1] * element[2])
            else:
                plnSales[str(element[0])] += (element[1] * element[2])
    pos = 0
    for k, v in plnSales.items():
        pos+=1
        conn.execute("INSERT INTO SalesCount (Id, Date, SalesPLN, SalesUSD)\
                        VALUES(?,?,?,?)", (pos, k, v, usdSales[k]))
    conn.commit()
    conn.close()
