from datetime import timedelta, datetime
from matplotlib.dates import drange, DateFormatter, DayLocator
import matplotlib.pyplot as plt

import lab4.rozwiazanie.work_with_db as db_conn


def print_plot_with_sales_data(start_date, end_date):

    db_data = db_conn.get_sales_list_from_db(start_date, end_date)
    dates = drange(datetime.strptime(db_data[0][0], "%Y-%m-%d").date(), (datetime.strptime(db_data[0][len(db_data[0])-1], "%Y-%m-%d")+ timedelta(days=1)).date(), timedelta(days=1))
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ratio = int(len(dates) / 10)
    interval = ratio if ratio > 0 else 1
    plt.gca().xaxis.set_major_locator(DayLocator(interval=interval))
    plt.plot(dates, db_data[1], dates, db_data[2])
    plt.gcf().autofmt_xdate()

    plt.xlabel('czas')
    plt.ylabel('')
    plt.title('Dzienna sprzedaż sklepu od ' + start_date + ' do ' + end_date)
    plt.legend(['USD', 'PLN'], loc='best')
    plt.savefig('shop_sales_chart.svg')
    plt.show()
