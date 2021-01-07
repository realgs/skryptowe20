import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


DATABASE = r"C:\Users\Patrycja\Desktop\5 semestr\Języki skryptowe\salesData.db"
MINDATE = '2013-01-04'
MAXDATE = '2016-12-29'


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS Rates (
                                            rDate date PRIMARY KEY,
                                            rValue real NOT NULL,
                                            rInterpolated bool NOT NULL
                                        ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def drop_table(conn):
    drop_table_sql = """DROP TABLE Rates"""
    try:
        c = conn.cursor()
        c.execute(drop_table_sql)
    except sqlite3.Error as e:
        print(e)


def delete_all_rates(conn):
    sql = """DELETE * FROM Rates"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def insert_data(conn, rate):
    sql = """ INSERT INTO Rates(rDate, rValue, rInterpolated)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, rate)
    conn.commit()


def fill_rates_data(conn):
    startdate = datetime.strptime(MINDATE, "%Y-%m-%d").date()
    enddate = datetime.strptime(MAXDATE, "%Y-%m-%d").date()
    minDate = startdate
    resp = nbp.get_avg_rates_date('USD', minDate, MAXDATE)
    rates = []
    dates = []
    for item in resp:
        rates.append((item['effectiveDate'], item['mid'], False))           # 3rd param - interpolated
        dates.append(item['effectiveDate'])
    print('Rates fetched before complement {}'.format(len(dates)))
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
            rates.append((date, value, True))               # 3rd param - interpolated
        startdate += timedelta(days=1)
    print('Rates fetched after complement {}'.format(len(rates)))
    for item in rates:
        insert_data(conn, item)


def get_rate(conn, date):
    """
    Query rate from given date
    :param conn: database connection
    :param date: YYYY-MM-DD
    :return: array of dictionaries containing the results
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Rates WHERE rDate=?", (date,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"Date": row[0], "Value": row[1], "Interpolated": bool(row[2])})
    return result


def get_multiple_rates(conn, startdate, enddate):
    """
    Query rates between given dates
    :param conn: database connection
    :param startdate: start date like YYYY-MM-DD
    :param enddate: end date like YYYY-MM-DD
    :return: array of dictionaries containing the results
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Rates WHERE rDate>=? AND rDate<=?", (startdate, enddate,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"Date": row[0], "Value": row[1], "Interpolated": bool(row[2])})
    return result


def get_all_sales(conn):
    """
    Query sales on given date
    :param conn: database connection
    :param date: YYYY-MM-DD
    :return: array of dictionaries containing the results
    """
    cur = conn.cursor()
    cur.execute("SELECT Rates.rDate, SUM(SalesOrder.sales), Rates.rValue "
                "FROM SalesOrder LEFT JOIN Rates ON SalesOrder.order_date=Rates.rDate "
                "GROUP BY Rates.rDate")
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"Date": row[0], "Sales": row[1], "RateValue": row[2]})
    return result


def get_sales(conn, date):
    """
    Query sales on given date
    :param conn: database connection
    :param date: YYYY-MM-DD
    :return: array of dictionaries containing the results
    """
    cur = conn.cursor()
    cur.execute("SELECT Rates.rDate, SUM(SalesOrder.sales), Rates.rValue "
                "FROM SalesOrder LEFT JOIN Rates ON SalesOrder.order_date=Rates.rDate "
                "WHERE rDate=?"
                "GROUP BY Rates.rDate", (date,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"Date": row[0], "Sales": row[1], "RateValue": row[2]})
    return result


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
        dataPLN.append(row[1] * row[2])
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
