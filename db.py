import sqlite3
import nbp
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS Rates (
                                            rDate date PRIMARY KEY,
                                            rValue real NOT NULL
                                        ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def delete_all_rates(conn):
    sql = 'DELETE FROM Rates'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def insert_data(conn, rate):
    sql = ''' INSERT INTO Rates(rDate, rValue)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, rate)
    conn.commit()


def fill_rates_data(conn):
    startdate = datetime.strptime('2013-01-04', "%Y-%m-%d").date()
    enddate = datetime.strptime('2016-12-29', "%Y-%m-%d").date()
    minDate=startdate
    resp = nbp.get_avg_rates_date('USD', minDate, '2016-12-29')
    rates = []
    dates = []
    for item in resp:
        rates.append((item['effectiveDate'], item['mid']))
        dates.append(item['effectiveDate'])
    print('Liczba notowań pobranych przed uzupełnieniem {}'.format(len(dates)))
    while startdate <= enddate:
        date = startdate.strftime("%Y-%m-%d")
        if date not in dates:
            value = 0.0
            lastdate = (datetime.strptime(date, "%Y-%m-%d").date() - timedelta(days=1)).strftime("%Y-%m-%d")
            hasvalue = False
            if datetime.strptime(lastdate, "%Y-%m-%d").date() < minDate:
                value = nbp.get_closest_one_day_rate('USD', date)[0]['mid']
            else:
                while lastdate not in dates:
                    lastdate = (datetime.strptime(lastdate, "%Y-%m-%d").date() - timedelta(days=1)).strftime("%Y-%m-%d")
                    if datetime.strptime(lastdate, "%Y-%m-%d").date() < minDate:
                        value = nbp.get_closest_one_day_rate('USD', date)[0]['mid']
                        hasvalue = True
                        break
                if not hasvalue:
                    value = rates[dates.index(lastdate)][1]
            rates.append((date, value))
        startdate += timedelta(days=1)
    print('Liczba notowań pobranych po uzupełnieniu {}'.format(len(rates)))
    for item in rates:
        insert_data(conn, item)


def select_data_and_plot(conn):
    cur = conn.cursor()
    cur.execute("SELECT Rates.rDate, SUM(SalesOrder.sales), Rates.rValue FROM SalesOrder JOIN Rates "
                "ON SalesOrder.order_date=Rates.rDate "
                "WHERE SalesOrder.order_date > '2016-08-30' "
                "GROUP BY Rates.rDate")
    rows = cur.fetchall()
    dates = []
    dataUSD = []
    dataPLN = []
    for row in rows:
        print(row)
        dates.append(datetime.strptime(row[0], "%Y-%m-%d"))
        dataUSD.append(row[1])
        dataPLN.append(row[1]*row[2])
    plot(dataUSD, dataPLN, 'Sprzedaż w USD', 'Sprzedaż w PLN', dates)


def plot(data1, data2, label1, label2, dates):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(dates, data1, label=label1)
    ax.plot(dates, data2, label=label2)
    ax.set_title('Łączna dzienna sprzedaż z ostatnich 120 dni 2016 roku')
    ax.legend(loc='upper left')
    ax.set_xlabel('Daty')
    ax.set_ylabel('Wartość')
    ax.set_xlim(xmin=min(dates), xmax=max(dates))
    plt.gcf().autofmt_xdate(rotation=25)
    fig.tight_layout()
    plt.show()
