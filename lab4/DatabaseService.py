import sqlite3
from datetime import date
from ApiService import getAverageExchangeRatesInDays


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
            exchange REAL NOT NULL
        )''')


def fillExchangeTable(dbCursor):
    exchangeRates = getAverageExchangeRatesInDays('usd', 730, date(2018, 5, 6))
    for item in exchangeRates:
        dbCursor.execute('INSERT INTO ExchangeUsdPln VALUES(NULL, ?,?)', (item.effectiveDate, item.mid))


if __name__ == '__main__':
    dbConnection = sqlite3.connect("nwdatabase.db")
    dbCursor = dbConnection.cursor()
    dropExchangeTable(dbCursor)
    createExchangeTable(dbCursor)
    fillExchangeTable(dbCursor)
    dbConnection.commit()
    dbConnection.close()
