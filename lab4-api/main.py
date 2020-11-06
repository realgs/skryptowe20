#!/bin/python3
import nbp
from nbp import Currency
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


if __name__ == "__main__":
    # 2. Wywołać funkcję pobierającą średnie kursy dolara amerykańskiego oraz euro z ostatniej połowy roku
    now = dt.now()
    half_year_from_now = now - relativedelta(months=6)

    half_year_rates_eur = nbp.rates_time_range(Currency.EUROPEAN_EURO, half_year_from_now, now)
    half_year_rates_usd = nbp.rates_time_range(Currency.UNITED_STATES_DOLLAR, half_year_from_now, now)

    print(half_year_rates_usd)
    print(half_year_rates_eur)
