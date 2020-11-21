import math

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def draw_currencies_chart(chart_data):
    currencies_rates_dates = []
    currencies_rates = []
    for currency_data in chart_data:
        current_rates = []
        current_dates = []
        for currency_price_with_date in currency_data[0]:
            current_dates.append(currency_price_with_date[0])
            current_rates.append(currency_price_with_date[1])
        currencies_rates.append(current_rates)
        currencies_rates_dates.append(current_dates)

    _, ax = plt.subplots()
    for index in range(len(currencies_rates)):
        ax.plot(currencies_rates_dates[index], currencies_rates[index], label=chart_data[index][1])

    max_dates_amount = 0
    for results in chart_data[0]:
        if max_dates_amount < len(results):
            max_dates_amount = len(results)
    tick_spacing = math.ceil(max_dates_amount / 5)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    plt.legend(loc=2, ncol=2)
    plt.title("Ceny walut przedstawione na przestrzeni czasu", loc='left', fontsize=12, fontweight=0)
    plt.xlabel("Data")
    plt.ylabel("Wartość w PLN")
    plt.show()
