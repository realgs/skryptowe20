import matplotlib.pyplot as plt


def sort_values_in_time_dict(exchange_rates_dict):
    return dict(sorted(exchange_rates_dict.items()))


def print_values_in_time(values_in_time_dicts, data_labels, ylabel, title):
    for i in range(len(values_in_time_dicts)):
        values_in_time_dicts[i] = sort_values_in_time_dict(values_in_time_dicts[i])
        x = list(values_in_time_dicts[i].keys())
        y = list(values_in_time_dicts[i].values())
        if(len(data_labels) > i):
            plt.plot(x, y, label = data_labels[i])
        else:
            plt.plot(x, y, label = "dane" + str(i))
    
    plt.xlabel("data")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()
