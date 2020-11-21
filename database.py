import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

import requests

DATABASE = 'database_files/Northwind.sqlite'
API_LIMIT = 366


def drawChartFromDatabase(start, end):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"""
   SELECT 
        date(OrderDate), 
        sum(UnitPrice * Quantity), 
        USD
   FROM 
        [Order] 
            JOIN OrderDetail ON [Order].Id = OrderDetail.OrderId 
            JOIN USDRates ON date(OrderDate) = RateDate
   WHERE 
        OrderDate BETWEEN '{start}' AND '{end}' 
   group by date(OrderDate)
   """)
    data = cursor.fetchall()
    days = []
    PlnEarnings = []
    UsdEarnings = []
    for sale in data:
        days.append(sale[0])
        UsdEarnings.append(sale[1])
        PlnEarnings.append(sale[2] * sale[1])
    drawChart(days, PlnEarnings, UsdEarnings)


def drawChart(days, PlnEarnings, UsdEarnings):
    plt.figure(figsize=(25, 7))
    dollar_line, = plt.plot(days, UsdEarnings, 'g', label='USD')
    pln_line, = plt.plot(days, PlnEarnings, 'r', label='PLN')
    plt.xticks(range(0, len(days), 30), days[::30], rotation=45, fontsize=10)
    plt.xlabel('Dates')
    plt.ylabel('Earnings in Mln $')
    plt.title('Daily earnings in USD and PLN')
    plt.legend(handles=[dollar_line, pln_line])
    plt.savefig("exercise5_label.svg")


def createTableUSD():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
                      CREATE TABLE USDRates   
                      (RateDate text, USD real)
                      ''')
    connection.commit()
    connection.close()


def fillUsdTable(dates, rates):
    USDPrices = []
    for i in range(0, len(dates)):
        queryData = (dates[i], rates[i])
        USDPrices.append(queryData)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.executemany('INSERT INTO USDRates VALUES (?,?)', USDPrices)
    connection.commit()
    connection.close()


def getUsdRates(start, end):
    start_date = start.date()
    end_date = end.date()
    dates_array = []
    rates_array = []
    while start_date != end_date:
        if start_date < end_date - timedelta(days=API_LIMIT):
            resp = requests.get(
                f"http://api.nbp.pl/api/exchangerates/rates/A/USD/{start_date}/{start_date + timedelta(days=API_LIMIT)}/")
            if resp.status_code == 200:
                for rate in resp.json()['rates']:
                    dates_array.append(rate['effectiveDate'])
                    rates_array.append(rate['mid'])
            else:
                print("Błąd połączenia")
            start_date = start_date + timedelta(days=(API_LIMIT + 1))
        else:
            resp = requests.get(
                f"http://api.nbp.pl/api/exchangerates/rates/A/USD/{start_date}/{end_date}/")
            if resp.status_code == 200:
                for rate in resp.json()['rates']:
                    dates_array.append(rate['effectiveDate'])
                    rates_array.append(rate['mid'])
            else:
                print("Błąd połączenia")
            start_date = end_date
    return dates_array, rates_array


def getCorrectedUsdRates(start, end, dates, rates):
    start_date = start.date()
    end_date = end.date()
    corrected_dates_array = []
    corrected_rates_array = []
    delta = end_date - start_date
    last_rate = 0
    delay = 0
    for i in range(delta.days + 1):
        date = start_date + timedelta(days=i)
        corrected_dates_array.append(date.strftime('%Y-%m-%d'))
        while i - delay >= len(dates):
            delay = delay + 1
        if str(dates[i - delay]) == str(date):
            last_rate = rates[i - delay]
            corrected_rates_array.append(last_rate)
        else:
            delay = delay + 1
            if last_rate != 0:
                corrected_rates_array.append(last_rate)
            else:
                resp = requests.get(
                    f"http://api.nbp.pl/api/exchangerates/rates/A/USD/{date - timedelta(days=1)}/")
                i = 2
                while resp.status_code != 200:
                    resp = requests.get(
                        f"http://api.nbp.pl/api/exchangerates/rates/A/USD/{date - timedelta(days=i)}/")
                    i = i + 1
                last_rate = resp.json()['rates'][0]['mid']
                corrected_rates_array.append(last_rate)
    return corrected_dates_array, corrected_rates_array


start_time = datetime(2013, 1, 1)
end_time = datetime(2015, 1, 1)
dates, rates = getUsdRates(start_time, end_time)
correct_dates, correct_rates = getCorrectedUsdRates(start_time, end_time, dates, rates)
createTableUSD()
fillUsdTable(correct_dates, correct_rates)
drawChartFromDatabase(start_time, end_time)
