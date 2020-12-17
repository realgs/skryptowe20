import sqlite3
from datetime import date, timedelta
from ApiService import getAverageExchangeRatesInDays
import copy


def getPricesUsdPlnInHalfYear():
    dbConnection = sqlite3.connect("nwdatabase.db")
    dbCursor = dbConnection.cursor()
    dbCursor.execute('''SELECT 
                    orderDate,
                    SUM(UnitPrice * Quantity*(1-Discount)) AS UsdPrice,
                    MAX(RateDate) AS RateDate,
                    Exchange,
                    SUM(UnitPrice * Quantity*(1-Discount)) * exchange AS PlnPrice
                    FROM "Order Details" NATURAL JOIN Orders JOIN ExchangeUsdPln On orderDate>=rateDate
                    WHERE OrderDate>="2017-11-06"
                    GROUP BY OrderDate''')
    result = dbCursor.fetchall()
    dbConnection.close()
    return result


def dropExchangeTable(dbCursor):
    dbCursor.execute('DROP TABLE IF EXISTS ExchangeUsdPln')


def createExchangeTable(dbCursor):
    dbCursor.execute('''
        CREATE TABLE IF NOT EXISTS ExchangeUsdPln(
            RateId INTEGER PRIMARY KEY ASC,
            RateDate DATETIME NOT NULL,
            exchange REAL NOT NULL,
            interpolated BIT NOT NULL
        )''')


def fillExchangeTable(dbCursor):
    exchangeRates = getAverageExchangeRatesInDays('usd', 730, date(2018, 5, 6))
    if not exchangeRates:
        return
    last = exchangeRates[0]
    for item in exchangeRates:
        while item.effectiveDate > last.effectiveDate:
            dbCursor.execute('INSERT INTO ExchangeUsdPln VALUES(NULL, ?,?,?)', (last.effectiveDate, last.mid, 1))
            last.effectiveDate += timedelta(days=1)
        dbCursor.execute('INSERT INTO ExchangeUsdPln VALUES(NULL, ?,?,?)', (item.effectiveDate, item.mid, 0))
        last = item
        last.effectiveDate += timedelta(days=1)


if __name__ == '__main__':
    dbConnection = sqlite3.connect("nwdatabase.db")
    dbCursor = dbConnection.cursor()
    dropExchangeTable(dbCursor)
    createExchangeTable(dbCursor)
    fillExchangeTable(dbCursor)
    dbConnection.commit()
    dbConnection.close()
