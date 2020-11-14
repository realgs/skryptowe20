import requests
from datetime import datetime, timedelta
import sqlite3


def create_sql_table():
    conn = sqlite3.connect('sql_data.db')
    cursor = conn.cursor()
    print("Database connected")

    cursor.execute('''CREATE TABLE USDPLN (ID, EffectiveDate, Rate);''')
    conn.commit()
    print("Table added")

    result = {}
    end_date = datetime.strptime('2018-12-31', '%Y-%m-%d')
    start_date = datetime.strptime('2016-01-01', '%Y-%m-%d')

    one_time_date = start_date - timedelta(1)
    prev_resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/{}/{}/{}/'.format("A", "USD", (one_time_date.strftime("%Y-%m-%d"))))

    while prev_resp.status_code != 200:
        one_time_date -= timedelta(1)
        prev_resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/{}/{}/{}/'.format("A", "USD", one_time_date.strftime("%Y-%m-%d")))

    while start_date < end_date:
        print("Adding rates for: " + start_date.strftime("%Y-%m-%d"))
        resp = requests.get(
            'http://api.nbp.pl/api/exchangerates/rates/{}/{}/{}/'.format("A", "USD", start_date.strftime("%Y-%m-%d")))
        if resp.status_code != 200 and prev_resp:
            result[start_date.strftime("%Y-%m-%d")] = prev_resp.json()['rates'][0]['mid']
        else:
            prev_resp = resp
            result[start_date.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']

        start_date += timedelta(days=1)

    i = 0
    for key, value in result.items():
        i += 1
        start_date = datetime.strptime(key, '%Y-%m-%d')
        conn.execute("INSERT INTO USDPLN (ID, EffectiveDate, Rate) \
                     VALUES (?, ?, ?)", (i, start_date.strftime("%d-%m-%Y"), value))
    conn.commit()
    conn.close()


create_sql_table()
