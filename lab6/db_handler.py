import sqlite3


def get_sales_data(date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM TotalSales WHERE date = ?", (date,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def get_sales_data_from_to(date_from, date_to):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM TotalSales WHERE date BETWEEN ? AND ?", (date_from, date_to))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def create_total_sales_table():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    ''' ExchangeRate table was created before, although I inserted all the available dates to it this time
    import api
    dates, rates = api.get_usd_exchange_rate_from_to(api.SALES_FROM_LIMIT, api.SALES_TO_LIMIT)
    results = api.fill_missing_data(api.SALES_FROM_LIMIT, api.SALES_TO_LIMIT, dates, rates)

    cursor.execute("CREATE TABLE ExchangeRate (date text, rate real)")
    for dict in results:
        cursor.execute("INSERT INTO ExchangeRate VALUES (?, ?)", (dict['rate']['date'], dict['rate']['rate']))
    connection.commit()
    '''

    cursor.execute("""SELECT date, rate, ROUND(order_sum, 4)
                      FROM ExchangeRate JOIN
                          (
                           SELECT DATE(O.OrderDate) order_date, SUM(OD.UnitPrice * OD.Quantity) order_sum
                           FROM OrderDetail OD JOIN `Order` O ON OD.OrderId = O.Id
                           GROUP BY DATE(O.OrderDate)
                          )
                      ON date = order_date;""")

    data = cursor.fetchall()
    cursor.execute("CREATE TABLE TotalSales(date text, sales_usd real, sales_pln real)")
    for i in range(len(data)):
        cursor.execute("INSERT INTO TotalSales VALUES (?, ?, ?)",
                       (data[i][0], data[i][2], round(data[i][2] * data[i][1], 2)))
    connection.commit()
    cursor.close()
    connection.close()
