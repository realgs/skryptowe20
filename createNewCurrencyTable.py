import sqlite3
import datetime
import requests
from datetime import date, datetime, timedelta

conn = sqlite3.connect('Cortland.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE CurrencyWithInterpolated (ID,Date,Currency,Interpolated);''')
conn.commit()

values = {}
interpolated = []

toDate = datetime.strptime('2020-10-10', '%Y-%m-%d')
fromDate = datetime.strptime('2018-10-10', '%Y-%m-%d')

tempDate = fromDate - timedelta(1)
getResp = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/a/usd/{tempDate.strftime("%Y-%m-%d")}/')

while getResp.status_code != 200:
    tempDate -= timedelta(1)
    getResp = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/a/usd/{tempDate.strftime("%Y-%m-%d")}/')

while fromDate < toDate:
    resp = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/a/usd/{fromDate.strftime("%Y-%m-%d")}/')

    if resp.status_code != 200:
        values[fromDate.strftime("%Y-%m-%d")] = getResp.json()['rates'][0]['mid']
        interpolated.append(True)
    else:
        getResp = resp
        values[fromDate.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']
        interpolated.append(False)   
    fromDate = fromDate + timedelta( days = 1)

id = 0
for key, value in values.items():
    id += 1
    dateNow = datetime.strptime(key, '%Y-%m-%d')
    conn.execute("INSERT INTO CurrencyWithInterpolated  (ID,Date,Currency,Interpolated)\
            VALUES(?,?,?,?)", (id, dateNow.strftime('%Y-%m-%d'), value, interpolated[id - 1]))

conn.commit()
conn.close()
        