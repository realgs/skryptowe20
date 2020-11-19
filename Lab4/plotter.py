import matplotlib.pyplot as plt
from date_parser import date_string_to_datetime
from constants import \
    PLOT_TITLE, \
    PLOT_XAXIS_LABEL, \
    PLOT_YAXIS_LABEL

def convert_rates(rates):
    dates = []
    values = []
    for r in rates:
        dates.append(date_string_to_datetime(r.effective_date))
        values.append(r.mid)

    return dates, values

def draw_rates_subplot(currency, rates):
    dates, values = convert_rates(rates)
    plt.plot(dates, values, label=f"{currency}")

def draw_rates(pairs):
    plt.figure()
    plt.subplot()
    for pair in pairs:
        draw_rates_subplot(pair[0], pair[1])
    plt.title(PLOT_TITLE)
    plt.xlabel(PLOT_XAXIS_LABEL)
    plt.ylabel(PLOT_YAXIS_LABEL)
    plt.legend()
    plt.show()

def convert_database_rates(rates):
    dates = []
    values = []
    for r in rates:
        dates.append(date_string_to_datetime(r[0]))
        values.append(r[1])

    return dates, values


def draw_database_subplot(currency, rates):
    dates, values = convert_database_rates(rates)
    plt.plot(dates, values, label=f"{currency}")

def draw_database(pairs):
    plt.figure()
    plt.subplot()
    for pair in pairs:
        draw_database_subplot(pair[0], pair[1])
    plt.title(PLOT_TITLE)
    plt.xlabel(PLOT_XAXIS_LABEL)
    plt.ylabel(PLOT_YAXIS_LABEL)
    plt.legend()
    plt.show()
