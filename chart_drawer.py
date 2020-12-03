import math

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def set_chart_data(plot, x_data, y_data, labels):
    _, ax = plot.subplots()
    for index in range(len(x_data)):
        ax.plot(x_data[index], y_data[index], label=labels[index])

    max_dates_amount = 0
    for dates in x_data:
        if max_dates_amount < len(dates):
            max_dates_amount = len(dates)
    tick_spacing = math.ceil(max_dates_amount / 5)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plot.legend(loc=2, ncol=2)


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

    labels = []
    for i in range(len(chart_data)):
        labels.append(chart_data[i][1])
    set_chart_data(plt, currencies_rates_dates, currencies_rates, labels)

    plt.title("Ceny walut przedstawione na przestrzeni czasu", loc='left', fontsize=12, fontweight=0)
    plt.xlabel("Data")
    plt.ylabel("Wartość w PLN")
    plt.savefig("EUR_USD_rates.svg")
    plt.show()


def draw_total_sales_chart(database_manager, date_from, date_to):
    total_sales = database_manager.get_total_sales(date_from, date_to)
    currency_rates = database_manager.get_currency_rates(date_from, date_to)

    dates = [[]]
    total_sale_sums = [[], []]
    for i in range(len(total_sales)):
        dates[0].append(total_sales[i][0])
        total_sale_sums[0].append(total_sales[i][1])
        for currency_rate in currency_rates:
            if total_sales[i][0] == currency_rate[0]:
                total_sales[i][1] = float(total_sales[i][1]) * currency_rate[1]
                break
        total_sale_sums[1].append(total_sales[i][1])
    dates.append(dates[0].copy())
    base_label_text = 'Suma sprzedaży w '
    labels = [
        base_label_text + 'USD',
        base_label_text + 'PLN'
    ]
    set_chart_data(plt, dates, total_sale_sums, labels)

    y_max = 500000
    plt.ylim(0, y_max)
    plt.title(f"Całkowita sprzedaż w okresie {date_from} - {date_to}", loc='right', fontsize=12, fontweight=0)
    plt.xlabel("Data")
    plt.ylabel("Suma")
    plt.savefig("total_sale_sum.svg")
    plt.show()
