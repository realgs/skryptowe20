import sqlite3
import requests
from datetime import date, datetime, timedelta

def createTable():
    conn = sqlite3.connect('Cortland.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE AverageRateToPLN (Number, DateCurrency, Value);''')
    conn.commit()
    values = {}

    toDate = datetime.strptime('2020-10-9', '%Y-%m-%d')
    fromDate = datetime.strptime('2018-10-10', '%Y-%m-%d')

    tempDate = fromDate - timedelta(1)
    getResp= requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/USD/{tempDate.strftime("%Y-%m-%d")}/')

    while getResp.status_code != 200:
        tempDate -= timedelta(1)
        getResp = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/USD/{tempDate.strftime("%Y-%m-%d")}/')

    while fromDate < toDate:
        resp = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/USD/{fromDate.strftime("%Y-%m-%d")}/')
        
        if resp.status_code != 200:
            values[fromDate.strftime("%Y-%m-%d")] = getResp.json()['rates'][0]['mid']
        else:
            getResp = resp
            values[fromDate.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']

        fromDate = fromDate + timedelta( days = 1)

    number = 0
    for first, second in values.items():
        number += 1
        tempFromDate = datetime.strptime(first, '%Y-%m-%d')
        conn.execute("INSERT INTO AverageRateToPLN (Number, DateCurrency, Value) \
                     VALUES (?, ?, ?)", (number, tempFromDate.strftime("%d-%m-%Y"), second))
                     
    conn.commit()
    conn.close()
