from matplotlib import pyplot as plt
import sqlite3
import csv
from datetime import date, timedelta
import requests

url = 'http://api.nbp.pl/api/exchangerates/rates/a/usd/'

conn = sqlite3.connect("orders.db")
c = conn.cursor()


def createOrdersDb():
    with conn:
        c.execute("CREATE TABLE orders (date text, cost real);")

        with open('orders.csv', 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['order_date'], i['unit_price']) for i in dr]

        c.executemany("INSERT INTO orders VALUES (?, ?);", to_db)


def createRatesDb():
    c.execute("""CREATE TABLE rates (
                date text,
                rate real)
    """)


def insertDateRate(date, rate):
    with conn:
        c.execute("INSERT INTO rates VALUES (?, ?)", (date, rate))


def updateRate(date, rate):
    with conn:
        c.execute("UPDATE rates SET rate=? WHERE date=?", (rate, date))


def getUsdRates(start, end):
    startYear = start.year
    endYear = end.year
    daysArray = []
    ratesArray = []
    if startYear != endYear:
        resp = requests.get(url + start.strftime('%Y-%m-%d') +
                            '/' + str(startYear) + '-12-31/')
        if resp.status_code != 200:
            print('GET ' + url + start.strftime('%Y-%m-%d') +
                  '/' + str(startYear) + '-12-31/\n' '{}'.format(resp.reason))
            pass
        else:
            for rate in resp.json()['rates']:
                daysArray.append(rate['effectiveDate'])
                ratesArray.append(rate['mid'])
            startYear = startYear + 1

    while startYear != endYear:
        resp = requests.get(url + str(startYear) + '-01-01/' + str(startYear) + '-12-31/')
        if resp.status_code != 200:
            print('GET ' + url + str(startYear) + '-01-01/' + str(startYear) + '-12-31/\n' '{}'.format(resp.reason))
            pass
        else:
            for rate in resp.json()['rates']:
                daysArray.append(rate['effectiveDate'])
                ratesArray.append(rate['mid'])
        startYear = startYear + 1

    resp = requests.get(url + str(endYear) + '-01-01/' + end.strftime('%Y-%m-%d') + '/')
    if resp.status_code != 200:
        print('GET ' + url + str(endYear) + '-01-01/' + end.strftime('%Y-%m-%d') + '/\n' '{}'.format(resp.reason))
        pass
    else:
        for rate in resp.json()['rates']:
            daysArray.append(rate['effectiveDate'])
            ratesArray.append(rate['mid'])
    return daysArray, ratesArray


def insertRates():
    start = date(2009, 1, 1)
    end = date(2012, 12, 30)
    delta = end - start
    day = start
    with conn:
        for i in range(delta.days + 1):
            day = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            insertDateRate(day, None)
        days, rates = getUsdRates(start, end)
        prevIndex = 0
        for i in range(delta.days + 1):
            day = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            if day in days:
                index = days.index(day)
                rate = rates[index]
                prevIndex = index
            else:
                rate = rates[prevIndex]
            updateRate(day, rate)


def showOrdersPlnUsd():
    with conn:
        ratesDict = {}
        dates = []
        ordersPln = []
        ordersUsd = []
        c.execute("SELECT * FROM rates")
        rates = c.fetchall()
        for rate in rates:
            ratesDict[rate[0]] = rate[1]

        c.execute("SELECT date, sum(cost) FROM orders GROUP BY date ORDER BY date")
        orders = c.fetchall()
        for row in orders:
            ordersUsd.append(row[1])
            ordersPln.append(row[1] * ratesDict[row[0]])
            dates.append(row[0])
        createPlot(dates, ordersPln, dates, ordersUsd)


def createPlot(days1, rates1, days2, rates2):
    days_short = days1[::200]
    plt.xticks(range(0, len(days1), 200), days_short)
    plt.xticks(fontsize=6)
    plt.plot(days1, rates1, label="PLN")
    plt.plot(days2, rates2, label="USD")
    plt.xlabel('Date')
    plt.ylabel('Cost')
    plt.title('Daily shopping cost in USD and PLN')
    plt.legend()
    plt.savefig("ordersInUsdPln.svg")
    plt.show()


conn.commit()
# conn.close()
