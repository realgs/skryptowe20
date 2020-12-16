import sqlite3

DATABASE = r".\salesData.db"


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(e)
    return conn


def get_rate(conn, date):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Rates WHERE rDate=?", (date,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"Date": row[0], "Value": row[1], "Interpolated": bool(row[2])})
    return result


def get_multiple_rates(conn, startdate, enddate):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Rates WHERE rDate>=? AND rDate<=?", (startdate, enddate,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"Date": row[0], "Value": row[1], "Interpolated": bool(row[2])})
    return result


def get_all_sales(conn):
    cur = conn.cursor()
    cur.execute("SELECT Rates.rDate, SUM(SalesOrder.sales), Rates.rValue "
                "FROM SalesOrder LEFT JOIN Rates ON SalesOrder.order_date=Rates.rDate "
                "GROUP BY Rates.rDate")
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"Date": row[0], "Sales": row[1], "RateValue": row[2]})
    return result


def get_sales_date(conn, date):
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
