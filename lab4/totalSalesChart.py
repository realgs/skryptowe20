import numpy as np
import matplotlib.pyplot as plt


def create_chart_of_total_sales(currency_name, total_sales_list):
    date_list = __get_list(total_sales_list, 0)
    total_due_list = __get_list(total_sales_list, 1)
    currency_rate_list = __get_list(total_sales_list, 2)
    changed_currency_list = __change_currency(total_due_list, currency_rate_list)

    ax = plt.subplot()
    ax.plot(date_list, total_due_list, label="USD")
    plt.ylim(0.0,350000)
    ax.plot(date_list, changed_currency_list, label="PLN")

    ax.set_title('Total daily sales')
    ax.set_ylabel('Value', fontweight='bold')
    ax.set_xlabel('Date', fontweight='bold')
    plt.legend()
    plt.savefig("Total_daily_sales_chart.svg")
    plt.show()


def __get_list(total_sales_list, arg):
    data_list = []
    for row in total_sales_list:
        data_list.append(row[arg])
    return data_list


def __change_currency(total_due_list, currency_rate_list):
    new_list = []
    for i in range(len(total_due_list)):
        new_list.append(float(total_due_list[i]) * float(currency_rate_list[i]))
    return new_list

