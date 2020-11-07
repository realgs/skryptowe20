#!/bin/python3

import nbp
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from typing import List
from nbp import Currency, DATE_FORMAT
from dateutil.relativedelta import relativedelta

if __name__ == "__main__":
    # 2. Wywołać funkcję pobierającą średnie kursy dolara amerykańskiego oraz euro z ostatniej połowy roku
    now = dt.datetime.now()
    half_year_from_now = now - relativedelta(months=6)

    usd = Currency.UNITED_STATES_DOLLAR
    eur = Currency.EUROPEAN_EURO
    pln = Currency.POLISH_ZLOTY

    half_year_rates_eur = nbp.rates_time_range(eur, half_year_from_now, now)
    half_year_rates_usd = nbp.rates_time_range(usd, half_year_from_now, now)

    # 3. Dla pobranych danych stworzyć jeden wykres prezentujący zależności notowań dolara i euro od czasu.
    # Pamiętaj o legendzie, podpisaniu osi i wykresu. Zapisz wykres w formacie eps lub svg i wrzuć do repo.

    x_usd: List[dt.date] = []
    y_usd: List[float] = []
    for rate, rate_date in half_year_rates_usd:
        x_usd.append(rate_date)
        y_usd.append(rate)

    x_eur: List[dt.date] = []
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
    plt.plot(x_eur, y_eur, label=f"{eur.title} ({eur.code})")

    # plot usd
    plt.plot(x_usd, y_usd, label=f"{usd.title} ({usd.code})")

    plt.gcf().autofmt_xdate()

    plt.gca().set_xlim(xmin=min(x_eur[0], x_usd[0]))

    plt.xlabel("Time [YYYY-MM-DD]")
    plt.ylabel(f"Rate [{pln.code}]")
    plt.title(
        f"{eur.code} and {usd.code} rates from last 6 months (in {pln.code})")

    plt.legend()
    plt.grid(True)
    plt.show()
