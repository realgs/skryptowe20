import matplotlib.pyplot as plt


def create_chart_of_total_sales(data_list):
    date_list = __convert_to_single_list(data_list, 0)
    total_due_list = __convert_to_single_list(data_list, 1)
    currency_rate_list = __convert_to_single_list(data_list, 2)
    changed_currency_list = __currency_conversion(total_due_list, currency_rate_list)

    fig = plt.subplot()
    fig.plot(date_list, total_due_list, label="USD")
    plt.ylim(0.0, 350000)
    fig.plot(date_list, changed_currency_list, label="PLN")

    fig.set_title('Total daily sales')
    fig.set_ylabel('Value')
    fig.set_xlabel('Date')

    plt.legend()
    plt.savefig("total_sales_plot.svg")
    plt.show()


def __convert_to_single_list(data_list, arg):
    new_list = []
    for data in data_list:
        new_list.append(data[arg])
    return new_list


def __currency_conversion(total_due_list, currency_rate_list):
    new_total_due_list = []
    for i in range(len(total_due_list)):
        new_total_due_list.append(float(total_due_list[i]) * float(currency_rate_list[i]))
    return new_total_due_list
