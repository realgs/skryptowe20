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

def draw_subplot(currency, rates):
    dates, values = convert_rates(rates)
    plt.plot(dates, values, label=f"{currency}")

def draw_plot(pairs):
    plt.figure()
    plt.subplot()
    for pair in pairs:
        draw_subplot(pair[0], pair[1])
    plt.title(PLOT_TITLE)
    plt.xlabel(PLOT_XAXIS_LABEL)
    plt.ylabel(PLOT_YAXIS_LABEL)
    plt.legend()
    plt.show()