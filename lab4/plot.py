import matplotlib.pyplot as plt


def draw_plot(currency1, currency1_date_list, currency1_rates_list,
              currency2, currency2_date_list, currency2_rates_list):
    fig = plt.subplot()
    fig.plot(currency1_date_list, currency1_rates_list, label=currency1)
    fig.plot(currency2_date_list, currency2_rates_list, label=currency2)

    fig.set_xlabel('Date')
    fig.set_ylabel('Value in PLN')

    plt.title('Dependence of dollar and euro exchange rates')

    plt.legend()
    plt.savefig("plot.svg")
    plt.show()
