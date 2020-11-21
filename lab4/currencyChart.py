import numpy as np
import matplotlib.pyplot as plt


def create_chart_of_two_currency(currency1_name, currency1_date_list, currency1_mid_rates_list, currency2_name, currency2_date_list, currency2_mid_rates_list):
    ax = plt.subplot()
    ax.plot(currency1_date_list, currency1_mid_rates_list, label=currency1_name)
    ax.plot(currency2_date_list, currency2_mid_rates_list, label=currency2_name)

    ax.set_title('Time dependence of USD and EUR exchange rates')
    ax.set_ylabel('Value in PLN', fontweight='bold')
    ax.set_xlabel('Date', fontweight='bold')
    plt.legend()
    plt.savefig("Time_dependence_of_USD_and_EUR_echange_rates_chart.svg")
    plt.show()
