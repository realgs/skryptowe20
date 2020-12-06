import matplotlib.pyplot as plt


def create_chart_of_total_sales(total_sales_list, currency_rate_list):
    date_list = __get_list(total_sales_list, 0)
    total_due_list = __get_list(total_sales_list, 1)
    changed_currency_list = __change_currency(total_sales_list, currency_rate_list)

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


def __change_currency(total_sales_list, currency_rate_list):
    new_list = []
    for i in range(len(total_sales_list)):
        date = total_sales_list[i][0]
        total_due = total_sales_list[i][1]
        currency_only_date_list = __get_list(currency_rate_list, 0)
        currency_rate_index = currency_only_date_list.index(date)
        new_list.append(float(total_due) * float(currency_rate_list[currency_rate_index][1]))
    return new_list
