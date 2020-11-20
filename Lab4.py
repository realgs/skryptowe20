import datetime
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.dates as pltd
import matplotlib.ticker as plttk
import matplotlib.dates as mdates
import sqlite3

DAYS_IN_YEAR = 365
DAYS_LIMIT = 92


def daysRange(xDays):
    if not isinstance(xDays, int):
        raise TypeError('Wrong type of parameter (daysRange)')
    if xDays <= 0:
        raise ValueError('Negativ days (daysRange)')

    today = datetime.datetime.date(datetime.datetime.now())
    previousDate = today - datetime.timedelta(days=xDays)
    dateRanges = []

    while (today - previousDate).days > DAYS_LIMIT:
        prev = previousDate
        next = previousDate + datetime.timedelta(days=DAYS_LIMIT)
        dateRanges.append((prev, next))
        previousDate = next + datetime.timedelta(days=1)

    dateRanges.append((previousDate, today))

    return dateRanges


def apiUrl(table, currency, fromDate, toDate):
    if not table.isalpha() or not isinstance(currency, str) or not isinstance(fromDate,
                                                                              datetime.date) or not isinstance(toDate,
                                                                                                               datetime.date):
        raise TypeError('Wrong instance of one of the parameters (apiUrl)')
    if toDate < fromDate:
        raise ValueError('toDate < fromDate')

    return f'http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{fromDate}/{toDate}'


# Zad1
def midCurrFromXDays(currency, xDays):
    dateRanges = daysRange(xDays)
    results = []

    for dateR in dateRanges:
        aTableUrl = apiUrl('a', currency, dateR[0], dateR[1])
        ra = requests.get(aTableUrl)

        if ra.status_code != 200:
            raise ra.exceptions.RequestException(f"Request for {aTableUrl} returned code {ra.status_code}: {ra.text}")
        elif ra.status_code == 404:
            return None
        else:
            results.append(json.loads(ra.text))

    for i in range(1, len(results)):
        results[0]['rates'] = results[0]['rates'] + results[i]['rates']

    if len(results):
        return results[0]
    else:
        return results


# zad3
def drawUSDEUR(days):
    usd = midCurrFromXDays('usd', days)
    eur = midCurrFromXDays('eur', days)

    usd_time = [usdTime['effectiveDate'] for usdTime in usd['rates']]
    usd_value = [usdVal['mid'] for usdVal in usd['rates']]

    euro_time = [eurTime['effectiveDate'] for eurTime in eur['rates']]
    euro_value = [eurVal['mid'] for eurVal in eur['rates']]

    fig, ax = plt.subplots()
    usdx = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in usd_time]
    ax.plot(usdx, usd_value, label='usd')
    eurx = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in euro_time]
    ax.plot(eurx, euro_value, label='euro')
    plt.gca().xaxis.set_major_formatter(pltd.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_locator(pltd.DayLocator(interval=15))

    plt.gca().yaxis.set_major_locator(plttk.MultipleLocator(0.1))
    ax.xaxis_date()
    fig.autofmt_xdate()
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Value in PLN', fontsize=14)
    plt.title("USD and EUR rates from half a year")
    plt.legend(loc='lower center')
    plt.grid(True)
    plt.savefig("RateOfUSD_EUR.svg")
    plt.show()


# Zad4
# database from https://www.sqlitetutorial.net/sqlite-sample-database/
def createExchangeTale():
    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    c.execute('CREATE TABLE ExchangeRate(Id, date, price)')
    conn.commit()
    conn.close()


# insert from  2011-03-18 to 2013-07-11
def insertToExRate():
    conn = sqlite3.connect('chinook.db')
    cursor = conn.cursor()
    fromDate = datetime.datetime.strptime('2011-03-18', '%Y-%m-%d')
    toDate = datetime.datetime.strptime('2013-07-11', '%Y-%m-%d')
    dateToTable = {}
    while (toDate > fromDate):
        resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/{}/'.format(toDate.strftime("%Y-%m-%d")))
        if resp.status_code != 200:
            dateToTable[toDate.strftime("%Y-%m-%d")] = prev_resp.json()['rates'][0]['mid']
        else:
            prev_resp = resp
            dateToTable[toDate.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']
        toDate = toDate - datetime.timedelta(days=1)
    pos = 0
    for k, v in dateToTable.items():
        pos += 1
        todayDate = datetime.datetime.strptime(k, '%Y-%m-%d')
        conn.execute("INSERT INTO ExchangeRate(Id, date, price) VALUES (?,?,?)",
                     (pos, todayDate.strftime("%Y-%m-%d"), v))
    conn.commit()
    conn.close()


# Zad5 liczba danych w tej bazie byla mala i skrajna,
# ale nie chcialem dodawac nowych rekordow zeby wyszlo to jak najbardziej autentycznie
def drawSalesChart():
    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    c.execute("SELECT InvoiceDate, Total FROM invoices WHERE InvoiceDate BETWEEN '2011-03-18' AND '2013-07-11'")
    tr = c.fetchall()
    c.execute('SELECT date, price FROM ExchangeRate')
    ex = c.fetchall()
    conn.commit()
    conn.close()
    dataHandler(tr, ex)


def plotChart(sumUsd, sumPln, days):
    plt.title('Summary sales in PLN and USD')
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.plot(days, sumUsd, color='green', label='USD')
    plt.plot(days, sumPln, color='red', label='PLN')
    plt.gca().xaxis.set_major_locator(plttk.MultipleLocator(35))
    plt.gca().xaxis.set_minor_locator(plttk.MultipleLocator(6))
    plt.gca().yaxis.set_major_locator(plttk.MultipleLocator(12))
    plt.gca().yaxis.set_minor_locator(plttk.MultipleLocator(3))
    plt.grid(True)
    plt.legend(loc='lower center')
    plt.savefig("Sales20112013.svg")
    plt.show()


def dataHandler(transactions, exchange_rates):
    sumsUsd = []
    sumsPln = []
    dates = []
    for tr in transactions:
        for ex in exchange_rates:
            if ex[0] in tr[0]:
                dates.append(ex[0])
                sumsUsd.append(tr[1])
                sumsPln.append(tr[1] * ex[1])
                break
    plotChart(sumsUsd, sumsPln, dates)


if __name__ == '__main__':
    # print(daysRange(180))
    # print(daysRange(0))
    # print(daysRange(-123241))
    # print(daysRange("234324"))
    # print(daysRange(1000))
    print(apiUrl("a", "usd", datetime.date(2020, 5, 24), datetime.date(2020, 6, 24)))
    # print(apiUrl("a", 513, datetime.date(2020, 5, 24), datetime.date(2020, 6, 24)))
    # print(apiUrl("b", "usd", "wefewfew", datetime.date(2020, 5, 24)))
    # print(apiUrl("a", "usd", datetime.date(2020, 5, 24), 4324234))
    # print(apiUrl(4, "usd", datetime.date(2020, 5, 24), datetime.date(2020, 8, 24)))
    # print(apiUrl("a", "usd", datetime.date(2020, 5, 24), datetime.date(2020, 5, 21)))

    # Zad2
    # print(json.dumps(midCurrFromXDays('eur', DAYS_IN_YEAR // 2), indent=3))
    # print(json.dumps(midCurrFromXDays('usd', DAYS_IN_YEAR // 2), indent=3))
    # drawUSDEUR(DAYS_IN_YEAR//2)
    # insertToExRate()
    # drawSalesChart()
