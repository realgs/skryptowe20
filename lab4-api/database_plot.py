#!/bin/python3

from datetime import date
import database as db
from typing import List, Tuple
from nbp import DATE_FORMAT, Currency
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


if __name__ == "__main__":

    # 4. Stworzyć wykres przedstawiający łączną sprzedaż (sumę wszystkich zawartch transakcji)
    # wyrażoną w walucie transakcji (np. USD) oraz w walucie PLN (przeliczenie po kursie z danego dnia sprzedaży).
    # Wykres stwórz dla przedziału czasowego wybranego przy realizacji zadania 3. Pamiętaj o legendzie,
    # podpisaniu osi i wykresu. Zapisz wykres w formacie eps lub svg i wrzuć do repo. (4pkt)

    conn = db.create_connection(db.DATABASE_FILE)
    if conn:
        c = conn.cursor()
        c.execute('''   SELECT SUM(SalesOrder.sales), 
                               SUM(SalesOrder.sales)*UsdRatesPln.rate, 
                               SalesOrder.order_date
                        FROM SalesOrder
                        INNER JOIN UsdRatesPln 
                        ON SalesOrder.order_date=UsdRatesPln.rate_date
                        GROUP BY SalesOrder.order_date
                        ORDER BY SalesOrder.order_date;''')

        conn.commit()
        query: List[Tuple[float, float, dt.date]] = [(row[0], row[1], dt.datetime.strptime(
            row[2], DATE_FORMAT).date()) for row in c.fetchall()]

        x_dates: List[dt.date] = []
        y_usd: List[float] = []
        y_pln: List[float] = []

        sum_usd = 0
        sum_pln = 0
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
            ticker.FuncFormatter(lambda x, pos: '%1.1fM' % (x * 1e-6)))
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.5E6))
        plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(1E5))

        # plot usd
        usd = Currency.UNITED_STATES_DOLLAR
        plt.plot(x_dates, y_usd, label=f"{usd.name.title()} ({usd.code})")

        # plot pln
        plt.plot(x_dates, y_pln, label=f"Polish_Zloty (PLN)")

        plt.gcf().autofmt_xdate()
        plt.gca().set_ylim(ymin=0)
        plt.gca().set_xlim(xmin=x_dates[0])

        plt.xlabel("Date [YYYY-MM-DD]")
        plt.ylabel("Sales [in millions]")
        plt.title(
            f"Sales in USD and PLN")

        plt.legend()
        plt.grid(True)
        plt.show()
