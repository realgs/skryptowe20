import matplotlib.pyplot as plt
from date_parser import date_string_to_datetime
from constants import \
    PLOT_TITLE_RATES, \
    PLOT_XAXIS_LABEL, \
    PLOT_YAXIS_LABEL_RATES

def convert_rates(rates):
    dates = []
    values = []
    for r in rates:
        dates.append(date_string_to_datetime(r.date))
        values.append(r.value)

    return dates, values

def draw_wrapper(wrapper):
    dates, values = convert_rates(wrapper.rates)
    plt.plot(dates, values, label=f"{wrapper.currency}")

def draw_list_of_wrappers(list_of_wrappers,
                          title=PLOT_TITLE_RATES,
                          xaxis=PLOT_XAXIS_LABEL,
                          yaxis=PLOT_YAXIS_LABEL_RATES):
    plt.figure()
    plt.subplot()
    for wrapper in list_of_wrappers:
        draw_wrapper(wrapper)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.legend()
    plt.show()
