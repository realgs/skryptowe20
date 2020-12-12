import sqlite3
import requests
import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

# Create your views here.
l = 5
salesData = 'salesData.db'
text = "Wrong value"
format = "%Y-%m-%d"



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
                    rates['Interpolated'] = True
                else :
                    rates['Interpolated'] = False

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

    def get(self, request, curr = 'usd', days='2015-01-01'):
        if(curr == 'usd'):
            data = self.dataRates(days)
            if data == None or data == {}:
                data = {
                    text: days
                }
        elif(curr == 'sales'):
            data = self.valuesSales(days)
            if data == None or data == {}:
                data = {
                    text: days
                }
        else:
            data = {
                text: curr
            }
        return Response(data)

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
                dateNow=dateNow.strftime("%Y-%m-%d")))
        if resp.status_code != 200:
            resultDays[dateNow.strftime('%Y-%m-%d')] = prevResp.json()['rates'][0]['mid']
            interpolTable.append(True)
        else:
            prevResp = resp
            resultDays[dateNow.strftime('%Y-%m-%d')] = resp.json()['rates'][0]['mid']
            interpolTable.append(False)
        dateNow = dateNow - datetime.timedelta(days=1)
    position = 0
    for key, value in resultDays.items():
        position += 1
        dateNow = datetime.datetime.strptime(key, '%Y-%m-%d')
        conn.execute("INSERT INTO USDPLNAverangeCur (Id, DateValue, AverageCurrency, Interpolated)\
                VALUES(?,?,?,?)", (position, dateNow.strftime('%Y-%m-%d'), value, interpolTable[position - 1]))

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
