import sqlite3
import requests
import matplotlib.pyplot as matplotlib
import averageRates
import chartsAverageUSDPLN
import addTable
from datetime import date, datetime, timedelta


if __name__ == '__main__':    
        #averageRates.averageRateDays("EUR", 15)
        #dol, eur = averageRates.halfYearDolarEuro()
        #chartsAverageUSDPLN.halfYearChartEuroDolar(dol, eur)
        #addTable.createTable()
        chartsAverageUSDPLN.createChartUSDPLN()
