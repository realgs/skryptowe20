#!/bin/python3

import config
import database as db
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from typing import List, Tuple
from nbp import DATE_FORMAT, Currency


if __name__ == "__main__":

    # 4. Stworzyć wykres przedstawiający łączną sprzedaż (sumę wszystkich zawartch transakcji)
    # wyrażoną w walucie transakcji (np. USD) oraz w walucie PLN (przeliczenie po kursie z danego dnia sprzedaży).
    # Wykres stwórz dla przedziału czasowego wybranego przy realizacji zadania 3. Pamiętaj o legendzie,
    # podpisaniu osi i wykresu. Zapisz wykres w formacie eps lub svg i wrzuć do repo. (4pkt)

    conn = db.create_connection(config.mysql_config)
    if conn:
        with conn.cursor() as cur:
            cur.execute(''' SELECT SUM(SO.sales), 
                                   SUM(SO.sales*R.rate), 
                                   SO.order_date
                            FROM SalesOrder SO
                            INNER JOIN UsdRatePln R 
                            ON SO.order_date=R.rate_date
                            GROUP BY SO.order_date
                            ORDER BY SO.order_date;''')
            query: List[Tuple[float, float, dt.date]] = [
                (float(row[0]), float(row[1]), row[2]) for row in cur]
        conn.close()

        x_dates: List[dt.date] = []
        y_usd: List[float] = []
        y_pln: List[float] = []

        sum_usd = 0.0
        sum_pln = 0.0
        for sales_usd, sales_pln, sales_date in query:
            x_dates.append(sales_date)
            sum_usd += sales_usd
            sum_pln += sales_pln
            y_usd.append(sum_usd)
            y_pln.append(sum_pln)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))

        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=5))

        plt.gca().yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: '%1.1fM' % (x * 1e-6)))
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5e5))
        plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(1e5))

        usd = Currency.UNITED_STATES_DOLLAR
        pln = Currency.POLISH_ZLOTY

        # plot usd
        plt.plot(x_dates, y_usd, label=f"{usd.title} ({usd.code})")
        # plot pln
        plt.plot(x_dates, y_pln,  label=f"{pln.title} ({pln.code})")

        plt.gcf().autofmt_xdate()
        plt.gca().set_ylim(ymin=0)
        plt.gca().set_xlim(xmin=x_dates[0])

        plt.xlabel("Time [YYYY-MM-DD]")
        plt.ylabel("Sales [in millions]")
        plt.title(
            f"SuperStore - Total sales (in {usd.code} and {pln.code})")

        plt.legend()
        plt.grid(True)
        plt.show()
