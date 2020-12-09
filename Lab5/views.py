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

class TestView(APIView):

    def exchangeRates(self,currency,day):
        current = datetime.datetime.now()
        currentDate = current.strptime(self.makeDate(current),formatDay)
        date = current - datetime.timedelta(days=day)
        thisDate = date.strptime(self.makeDate(date),formatDay)
        tempresp=requests.get('http://api.nbp.pl/api/exchangerates/rates/a/{currency}/last/1'.format(currency=currency))
        if tempresp.status_code!=success: return None
        else:
            prev_resp=requests.get('http://api.nbp.pl/api/exchangerates/rates/a/{currency}/last/1'.format(currency=currency))
            salesDate=[]
            while (currentDate > thisDate):
                resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{day}/'.format(currency=currency,day=self.makeDate(currentDate)))
                sales = {}
                sales['No'] = prev_resp.json()[rates][0][no]
                sales['Date'] = self.makeDate(currentDate)
                if resp.status_code != success:
                   sales['Rate']=prev_resp.json()[rates][0][mid]
                   sales['Interpolated'] = True
                else:
                    prev_resp = resp
                    sales['Rate'] = resp.json()[rates][0][mid]
                    sales['Interpolated'] = False
                salesDate.append(sales)
                currentDate = currentDate - datetime.timedelta(days=next)
            return salesDate

    def sales(self,date):
        conn = sqlite3.connect(dataBase)
        cursor = conn.cursor()
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
        sales = {}
        if(salesPLN.__contains__(date)):
            sales['Date']=date
            sales['Sales in PLN'] = salesPLN[date]
            sales['Sales in USD'] = salesUSD[date]
            return sales
        else: return None

    def makeDate(self,date):
        thisDate = date.strftime(formatDay)
        return thisDate

    def get(self,request,currency='USD',days=1):
        if(len(currency)<l):
            data = self.exchangeRates(currency,days)
            if data == None:
                data = {
                    'Zła waluta': currency
                }
        else:
            data=self.sales(currency)
            if data == None:
                data = {
                    'Zła data': currency
                }
        return Response(data)



