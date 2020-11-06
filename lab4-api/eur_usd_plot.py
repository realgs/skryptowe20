#!/bin/python3
from typing import List
import nbp
from nbp import Currency, DATE_FORMAT
import datetime as dt
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

if __name__ == "__main__":
    # 2. Wywołać funkcję pobierającą średnie kursy dolara amerykańskiego oraz euro z ostatniej połowy roku
    now = dt.datetime.now()
    half_year_from_now = now - relativedelta(months=6)

    usd = Currency.UNITED_STATES_DOLLAR
    eur = Currency.EUROPEAN_EURO

    half_year_rates_eur = nbp.rates_time_range(eur, half_year_from_now, now)
    half_year_rates_usd = nbp.rates_time_range(usd, half_year_from_now, now)

    # 3. Dla pobranych danych stworzyć jeden wykres prezentujący zależności notowań dolara i euro od czasu.
    # Pamiętaj o legendzie, podpisaniu osi i wykresu. Zapisz wykres w formacie eps lub svg i wrzuć do repo.

    x_usd: List[str] = []
    y_usd: List[float] = []
    for rate, rate_date in half_year_rates_usd:
        x_usd.append(rate_date)
        y_usd.append(rate)

    x_eur: List[str] = []
    y_eur: List[float] = []
    for rate, rate_date in half_year_rates_eur:
        x_eur.append(rate_date)
        y_eur.append(rate)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))

    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=1))

    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.05))
    plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(0.01))

    # plot euro
    plt.plot(x_eur, y_eur, label=f"{eur.name.title()} ({eur.code})")

    # plot usd
    plt.plot(x_usd, y_usd, label=f"{usd.name.title()} ({usd.code})")

    plt.gcf().autofmt_xdate()

    plt.xlabel("Date [YYYY-MM-DD]")
    plt.ylabel("Rate [PLN]")
    plt.title(f"{eur.code} and {usd.code} rates from last 6 months (in PLN)")

    plt.legend()
    plt.grid(True)
    plt.show()
