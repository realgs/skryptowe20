from datetime import date, timedelta, datetime
import requests
from mongoengine import *
from copy import copy
import sqlite3

CurrURL = "http://api.nbp.pl/api/exchangerates/tables/{}"
ExchangeURL = "http://api.nbp.pl/api/exchangerates/rates/{}/{}/{}/{}/"
connect(host="mongodb+srv://Skryptowe:yArfxRUIvpFQii7p@cluster0.gcuoh.mongodb.net/currency-and-sales?retryWrites=true&w"
             "=majority")
dateFormat = '%Y-%m-%d'


class Exchange(Document):
    code = StringField(max_length=3)
    dateStr = StringField()
    date = DateField()
    mid = FloatField()
    interpolated = BooleanField()


class SalesResult(Document):
    dateStr = StringField()
    date = DateField()
    usd = FloatField()
    pln = FloatField()


def getCurrencyList(table):
    currencyList = []
    resp = requests.get(CurrURL.format(table))
    for i in resp.json()[0]['rates']:
        currencyList.append(i['code'])
    return currencyList


def getAllExchangeRatesForTable(currencyList, table):
    exchangeRates = {}
    for curr in currencyList:
        exchangeRates[curr] = fillGapsInExchangeList(getExchangeRatesForOneCurrency(curr, table))
    return exchangeRates


def getExchangeRatesForOneCurrency(code, table, startDate=date(2002, 1, 2)):
    endDate = startDate + timedelta(days=367)
    if endDate > date.today():
        endDate = date.today()
    exchangeRates = []
    resp = requests.get(ExchangeURL.format(table, code, startDate, endDate))
    if resp.status_code == 200:
        resp = resp.json()
        for rate in resp['rates']:
            rate['effectiveDate'] = datetime.strptime(rate['effectiveDate'], dateFormat).date()
            exchangeRates.append(rate)
    if endDate == date.today():
        return exchangeRates
    return exchangeRates + getExchangeRatesForOneCurrency(code, table, endDate + timedelta(days=1))


def fillGapsInExchangeList(exchangeList):
    filledList = []
    lastExchange = exchangeList[0]
    for ex in exchangeList:
        ex['interpolated'] = False
        while lastExchange['effectiveDate'] < ex['effectiveDate']:
            filledList.append(copy(lastExchange))
            lastExchange['effectiveDate'] += timedelta(days=1)
        filledList.append(ex)
        lastExchange = copy(ex)
        lastExchange['effectiveDate'] += timedelta(days=1)
        lastExchange['interpolated'] = True
    lastExchange = copy(filledList[len(filledList) - 1])
    lastExchange['interpolated'] = True
    while lastExchange['effectiveDate'] < date.today():
        lastExchange['effectiveDate'] += timedelta(days=1)
        filledList.append(copy(lastExchange))
    return filledList


def fillExchanges(exchangeRates):
    exchanges = []
    for curr in exchangeRates:
        for rate in exchangeRates[curr]:
            exchanges.append(Exchange(
                code=curr,
                dateStr=rate['effectiveDate'].strftime(dateFormat),
                date=rate['effectiveDate'],
                mid=rate['mid'],
                interpolated=rate['interpolated']
            ))
    Exchange.objects.insert(exchanges)


def fillSales(sales):
    salesResults = []
    for sale in sales:
        ex = Exchange.objects(code='USD', dateStr=sale[0]).first()
        salesResults.append(SalesResult(
            dateStr=sale[0],
            date=ex.date,
            usd=sale[1],
            pln=sale[1] * ex.mid
        ))
    SalesResult.objects.insert(salesResults)


def getSales():
    conn = sqlite3.connect('nwdatabase.db')
    curr = conn.cursor()
    curr.execute('''SELECT 
                        orderDate,
                        SUM(UnitPrice * Quantity*(1-Discount))
                        FROM "Order Details" NATURAL JOIN Orders
                        GROUP BY OrderDate''')
    result = curr.fetchall()
    conn.close()
    return result


def fillDB():
    fillExchanges(getAllExchangeRatesForTable(getCurrencyList('A'), 'A'))
    fillExchanges(getAllExchangeRatesForTable(getCurrencyList('B'), 'B'))
    fillSales(getSales())


def apiTest():
    usd = requests.get('http://127.0.0.1:5000/rates/eur/2020-12-20').json()
    print(usd)
    sale = requests.get('http://127.0.0.1:5000/sales/2017-01-01').json()
    print(sale)


if __name__ == '__main__':
    # fillDB()
    apiTest()
