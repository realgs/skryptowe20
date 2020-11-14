import matplotlib.pyplot as plt


def plot_dollar_euro(dollars, euros):
    dollar_dates = []
    dollar_rates = []
    euro_dates = []
    euro_rates = []

    for key, value in dollars.items():
        dollar_dates.append(key)
        dollar_rates.append(value)
    dollar_rates.reverse()
    dollar_dates.reverse()
    for key, value in euros.items():
        euro_dates.append(key)
        euro_rates.append(value)
    euro_dates.reverse()
    euro_rates.reverse()

    ay, ax = plt.subplots()
    dollar_line, = plt.plot(dollar_dates, dollar_rates, 'g', label='Dollar')
    euro_line, = plt.plot(euro_dates, euro_rates, 'r', label='Euro')
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % 10 != 0:
            label.set_visible(False)

    plt.title('Dollar and Euro rates')
    plt.xlabel('Dates')
    plt.ylabel('Rates')
    plt.xticks(rotation=60, fontsize=6)
    plt.legend(handles=[dollar_line, euro_line])
    plt.savefig("exercise3.svg")
    plt.show()
