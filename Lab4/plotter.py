
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
from date_parser import date_string_to_datetime

def convert_rates(rates):
    dates = []
    values = []
    for r in rates:
        dates.append(date_string_to_datetime(r.effective_date))
        values.append(r.mid)

    return dates, values

def draw_plot(rates):
    dates, values = convert_rates(rates)
    plt.figure()
    plt.subplot()
    plt.plot(dates, values, label="USD")
    plt.title("Pieniążki")
    plt.legend()
    plt.show()