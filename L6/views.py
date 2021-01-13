import sqlite3
import requests
import datetime
import matplotlib.pyplot as plt
from rest_framework.views import APIView
from django.shortcuts import render

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

#metoda dodająca tabelę z nową kolumną interpolated i wypełniająca ją, uruchomiona tylko raz
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

#metoda dodająca tabelę z sumowanymi sprzedażami i wypełniająca ją, uruchomiona tylko raz
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
    def chartRates(self,startDate,endDate):
        dates=[]
        rates=[]
        conn = sqlite3.connect(dataBase)
        cursor = conn.cursor()
        cursor.execute('''SELECT Id,DateOfValue,AverageCurrency
                                    FROM AverageCurrencyUSDPLN''')
        for elem in cursor:
            if datetime.datetime.strptime(elem[1],formatDay)>=datetime.datetime.strptime(startDate,formatDay) and datetime.datetime.strptime(elem[1],formatDay)<=datetime.datetime.strptime(endDate,formatDay):
                dates.append(elem[1])
                rates.append(elem[2])
        conn.close()
        return (dates,rates)

    def chartSales(self, startDate, endDate):
        dates = []
        plnsales = []
        usdsales=[]
        conn = sqlite3.connect(dataBase)
        cursor = conn.cursor()
        cursor.execute('''SELECT Id,DateOfSale,SalesPLN,SalesUSD
                                            FROM SumOfSales''')
        for elem in cursor:
            if datetime.datetime.strptime(elem[1], formatDay) >= datetime.datetime.strptime(startDate, formatDay) and datetime.datetime.strptime( elem[1], formatDay) <= datetime.datetime.strptime(endDate, formatDay):
                dates.append(elem[1])
                plnsales.append(elem[2])
                usdsales.append(elem[3])
        conn.close()
        return (dates, plnsales,usdsales)

    def get(self, request, *args, **kwargs):
        date = request.GET.get('dateusd')
        date2 = request.GET.get('salesusd')
        startDay = request.GET.get('dateusdstart')
        endDay = request.GET.get('dateusdend')
        startsales = request.GET.get('datesalesstart')
        endsales = request.GET.get('datesalesend')
        if(startDay != None and endDay != None):
            (dates, rates) = self.chartRates(startDay, endDay)
            if len(dates) == 0:
                mes = {"message": "We don't have data from this date"}
                return render(request, "HomePage.html", mes)
            dates.reverse()
            rates.reverse()
            plt.plot(dates, rates)
            if(len(dates) > 20):
                datesShort = dates[::20]
                plt.xticks(range(0, len(dates), 20), datesShort)
            plt.title(f"Average Exchange Rates of USD from {startDay} to {endDay}")
            plt.xlabel('Dates')
            plt.ylabel('Average Exchange Rates')
            plt.grid(True)
            plt.gcf().autofmt_xdate(rotation=25)
            plt.savefig('C:\\Users\\oladr\\PycharmProjects\\skryptoweAPI2\\skryptoweAPIDJ\\static\\images\\USD_Chart2.png')
            plt.close()

        if (startsales != None and endsales != None):
            (datesSales, salesPLN, salesUSD) = self.chartSales(startsales, endsales)
            if len(datesSales) == 0:
                mes2 = {"message2" : "We don't have data from this date"}
                return render(request, "HomePage.html", mes2)
            datesSales.reverse()
            salesPLN.reverse()
            salesUSD.reverse()
            plt.plot(datesSales, salesPLN)
            plt.plot(datesSales, salesUSD)
            if (len(datesSales) > 20):
                datesSalesShort = datesSales[::20]
                plt.xticks(range(0, len(datesSales), 20), datesSalesShort)
            plt.title(f"Sales in PLN and USD from {startsales} to {endsales}")
            plt.xlabel('Dates')
            plt.ylabel('Sales')
            plt.legend(['PLN Sales', 'USD Sales'])
            plt.grid(True)
            plt.gcf().autofmt_xdate(rotation=25)
            plt.savefig('C:\\Users\\oladr\\PycharmProjects\\skryptoweAPI2\\skryptoweAPIDJ\\static\\images\\Sales_Chart2.png')
            plt.close()
        dataUSD = self.exchangeRates(date)
        salesUSD=self.sales(date2)
        dataUSD2 = {}
        dataUSD3 = {}
        if dataUSD.get('Id') != None:
            dataUSD2['Id'] = dataUSD.get('Id')
            dataUSD2['Date'] = dataUSD.get('Date')
            dataUSD2['Rate'] = dataUSD.get('Rate of USD')
            dataUSD2['Interpolated'] = dataUSD.get('Interpolated')
            return render(request, "HomePage.html", dataUSD2)
        if salesUSD.get('Id') != None:
            dataUSD3['Id2'] = salesUSD.get('Id')
            dataUSD3['Date2'] = salesUSD.get('Date')
            dataUSD3['PLN'] = salesUSD.get('Sales in PLN')
            dataUSD3['USD'] = salesUSD.get('Sales in USD')
            return render(request, "HomePage.html", dataUSD3)
        return render(request, "HomePage.html")
