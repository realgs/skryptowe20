import sqlite3
import api_chart as ac
import datetime
import matplotlib.pyplot as plt


def extract_to_chart_data(db_data):
    dates = []
    usd_sales = []
    pln_sales = []

    for i in range(len(db_data)):
        dates.append(datetime.datetime.strptime(db_data[i][0], ac.DATE_FORMAT))
        usd_sales.append(db_data[i][2])
        pln_sales.append(round(db_data[i][1]*db_data[i][2], 2))

    return dates, usd_sales, pln_sales


def create_table():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    dates, rates = ac.average_exchange_rates_between("USD", "2012-07-20", "2016-02-19")
    all_dates, all_rates = ac.fill_missing_data("2012-07-20", "2016-02-19", dates, rates)

    # cursor.execute("CREATE TABLE ExchangeRate (date text, rate real)")

    # for i in range(len(all_dates)):
    #    cursor.execute("INSERT INTO ExchangeRate VALUES (?, ?)", (all_dates[i], all_rates[i]))

    # connection.commit()

    cursor.execute("""SELECT date, rate, ROUND(order_sum, 4)
                      FROM ExchangeRate JOIN
                          (
                           SELECT DATE(O.OrderDate) order_date, SUM(OD.UnitPrice * OD.Quantity) order_sum
                           FROM OrderDetail OD JOIN `Order` O ON OD.OrderId = O.Id
                           GROUP BY DATE(O.OrderDate)
                          )     
                      ON date = order_date;""")

    db_data = cursor.fetchall()
    cursor.close()
    connection.close()

    return db_data


def plot_db_data(db_data):
    dates, usd_sales, pln_sales = extract_to_chart_data(db_data)

    plt.plot(dates, usd_sales, label="USD")
    plt.plot(dates, pln_sales, label="PLN")

    plt.gcf().autofmt_xdate()
    plt.xlabel('Date [YYYY-MM-DD]')
    plt.ylabel('Earnings [USD/PLN]')
    plt.legend(['Earnings in USD', 'Earnings in PLN'])
    plt.title('Daily earnings in USD and PLN')
    plt.show()


if __name__ == '__main__':
    db_data = create_table()
    plot_db_data(db_data)
