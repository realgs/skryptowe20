import sqlite3
import zad1
import zad4

conn = sqlite3.connect("orders.db")

if __name__ == "__main__":
    zad1.showUsdEurRates()

    zad4.createRatesDb()
    zad4.insertRates()
    zad4.showOrdersPlnUsd()

    conn.commit()
    conn.close()
