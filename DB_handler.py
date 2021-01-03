import sqlite3
import NBP_currency
import const


def get_orders_in_pln_and_usd(start, end):
    conn = sqlite3.connect('chinook.db')
    cur = conn.cursor()
    cur.execute(f"SELECT InvoiceDate, Total FROM invoices WHERE InvoiceDate BETWEEN '{start}' AND '{end}'")
    rates_dict = NBP_currency.get_daily_currency_rates(start, end, const.USD_CURRENCY)
    all_orders = cur.fetchall()
    daily_orders = {}
    currency1 = const.USD_CURRENCY
    currency2 = const.PLN_CURRENCY
    for order in all_orders:
        daily_orders[order[0][:10]] = {}
        daily_orders[order[0][:10]][currency1] = round(order[1],2)
        daily_orders[order[0][:10]][currency2] = round(order[1] * rates_dict[order[0][:10]]['rate'],2)
    if daily_orders == {}:
        return 404
    conn.close()
    return daily_orders
