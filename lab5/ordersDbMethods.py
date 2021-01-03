import sqlite3
import csv
import currencyMethods


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_orders_db():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE orders (date text, cost real);")

    with open('orders.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['order_date'], i['unit_price']) for i in dr]

    cur.executemany("INSERT INTO orders VALUES (?, ?);", to_db)


def get_orders_in_pln_and_usd(start, end):
    conn = sqlite3.connect('orders.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    cur.execute(f"""SELECT [date], sum(cost) "orders_cost_in_usd"
                    FROM orders
                    WHERE [date] BETWEEN '{start}' AND '{end}'
                    GROUP BY [date]
                    ORDER BY [date]""")
    rates_dict = currencyMethods.get_daily_currency_rates(start, end, "usd")
    all_orders = cur.fetchall()
    if all_orders == {}:
        return 404
    daily_orders = {}
    currency1 = "orders_cost_in_usd"
    currency2 = "orders_cost_in_pln"
    for order in all_orders:
        daily_orders[order['date']] = {}
        daily_orders[order['date']][currency1] = order[currency1]
        daily_orders[order['date']][currency2] = order[currency1] * rates_dict[order['date']]['rate']
    if daily_orders == {}:
        return 404
    conn.close()
    return daily_orders
