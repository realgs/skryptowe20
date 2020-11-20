#!/usr/bin/python3

import sqlite3
import datetime
import database
import currency_API
# import plotting

DATABASE_NAME = "sales_data.db"
HALF_YEAR_DAYS = 183

def plot_sales_data(cursor, date_from, date_to):
    sales_data = database.select_sales_data(cursor, date_from, date_to)
    sales_plot_data = {}

    for item in sales_data:
        sales_plot_data[currency_API.string_to_datetime(item[0])] = (item[1], item[2])

    sales_plot_description = \
    {
        'title': 'sprzedaż z dni ' + date_from.strftime("%Y-%m-%d") + ' - ' + date_to.strftime("%Y-%m-%d"),
        'x_label': 'data',
        'y_label': 'kwota',
        'data_labels': ('PLN', 'USD')
    }
    plotting.plot_dictionary(sales_plot_data, sales_plot_description)

def plot_markings_data(currency_list, days):
    markings_plot_data = currency_API.get_recent_currency_list_markings(currency_list, days)
    plot_title = "notowania "

    for currency_code in currency_list:
        plot_title += currency_code + ', '

    markings_plot_description = \
    {
        'title': plot_title[:-2],
        'x_label': 'data',
        'y_label': 'średnia cena [PLN]',
        'data_labels': currency_list
    }
    plotting.plot_iterable(markings_plot_data, markings_plot_description)

if __name__ == "__main__":
    database_from = currency_API.string_to_datetime('2014-10-16')
    database_to = currency_API.string_to_datetime('2016-10-16')

    CHF_data = currency_API.get_recent_currency_markings('CHF', 370)

    for x in CHF_data.keys():
        print(x, ':', CHF_data[x])

    plot_markings_data(['USD', 'EUR'], HALF_YEAR_DAYS)

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # database.assure_markings(cursor)
    database.refill_markings(cursor, 'USD', database_from, database_to)
    connection.commit()
    plot_sales_data(cursor, database_from, database_to)

    connection.close()
