import matplotlib.pyplot as plt
import requests
import sqlite3
from enum import Enum
from datetime import datetime, timedelta

LIMIT = 366


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    PLN = 'PLN'
    CHF = 'CHF'


def make_request(currency, start_date, end_date):
    if currency not in Currency._value2member_map_ or not 0 < (end_date - start_date).days <= LIMIT:
        print('Invalid arguments, please try again')
    else:
        response = requests.get(
            f'http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date.date()}/{end_date.date()}/?format=json')
        if(response.status_code != 200):
            print(f'Request Error {response.status_code}')
            return response.status_code
        else:
            return response


def to_date(date):
    if isinstance(date, datetime):
        return date
    else:
        return datetime.strptime(date, '%Y-%m-%d')


def fix_response(response):
    x = []
    previous_date = response.json()['rates'][0]
    for value in response.json()['rates']:
        for date in range(1, (to_date(value['effectiveDate']) - to_date(previous_date['effectiveDate'])).days):
            x.append((to_date(previous_date['effectiveDate']) + timedelta(days=date), previous_date['mid'], True))
        x.append((to_date(value['effectiveDate']), value['mid'], False))
        previous_date = value

    return x


def get_currency(currency, start_date, end_date):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM CURRENCY WHERE SYMBOL = ?
            AND DATE BETWEEN ? AND ?''', currency.upper(), start_date(), end_date())
    return c.fetchall()


def update_sales_stats():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    duplicates = 0
    x = []
    for row in c.execute('''SELECT SUM(SALES), ORDERDATE FROM SALES
                            GROUP BY ORDERDATE
                            ORDER BY ORDERDATE'''):
        x.append(row)

    for row in x:
        try:
            safe_data = (int(row[1]), float(row[0]))
            c.execute('INSERT INTO sales_stats VALUES(?, ?)', safe_data)
        except(sqlite3.IntegrityError):
            duplicates += 1

    print(f'{duplicates} values were already in database')
    conn.commit()
    conn.close()


def get_range(currency, start_date, end_date):
    dates = split_date(start_date, end_date)
    x = []
    for date_range in dates:
        response = make_request(currency, date_range[0], date_range[1])
        if isinstance(response, int) or response is None:
            print(f'Failed fetching data between {date_range[0]} and {date_range[1]}')
        else:
            x.append(fix_response(response))

    return [item for subl in x for item in subl]


def fill_currency(currencies, start_date, end_date):
    for currency in currencies:
        currencyValues = get_range(currency, start_date, end_date)
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        print("Opened database successfully")
        duplicates = 0
        for daily_value in currencyValues:
            try:
                safe_data = (currency.upper(), daily_value[0].timestamp(), daily_value[1], daily_value[2], )
                c.execute('INSERT INTO currency VALUES(?,?,?,?)', safe_data)
            except sqlite3.IntegrityError:
                duplicates += 1

        if duplicates != 0:
            print(f'{duplicates} values were not added to database due to Integrity Error')
        conn.commit()
        conn.close()


def split_date(start_date, end_date):
    days_between = (to_date(end_date) - to_date(start_date)).days
    dates = []
    while days_between != 0:
        if days_between >= LIMIT:
            dates.append((to_date(end_date) - timedelta(days=days_between), to_date(end_date) -
                          timedelta(days=days_between) + timedelta(days=LIMIT - 1)))
            days_between -= LIMIT
        else:
            dates.append((to_date(end_date) - timedelta(days=days_between), to_date(end_date)))
            days_between = 0
    return dates


# def get_sales(start_date, end_date):
#     if (to_date(end_date) - to_date(start_date)).days < 0:
#         print('Illegal argument')
#     conn = sqlite3.connect('sales.db')
#     c = conn.cursor()
#     print("Opened database successfully")
#     x = {}
#     previous_sales = 0

#     safe_date = (to_date(start_date).timestamp(), to_date(end_date).timestamp(),)
#     for row in c.execute('''SELECT SUM(SALES), ORDERDATE FROM SALES
#                             WHERE ORDERDATE between ? and ?
#                             GROUP BY ORDERDATE
#                             ORDER BY ORDERDATE''', safe_date):
#         x[datetime.fromtimestamp(int(row[1])).date()] = x.get(
#             datetime.fromtimestamp(int(row[1])).date(), 0) + float(row[0])

#     for key in x.keys():
#         x[key] += previous_sales
#         previous_sales = x[key]

#     conn.close()
#     return x


# def get_currency(start_date, end_date):
#     if (to_date(end_date) - to_date(start_date)).days < 0:
#         print('Illegal argument')
#     conn = sqlite3.connect('sales.db')
#     c = conn.cursor()
#     print("Opened database successfully")
#     x = {}

#     safe_date = (to_date(start_date).timestamp(), to_date(end_date).timestamp(),)
#     for row in c.execute('SELECT value, date from currency where date between ? and ? ORDER BY date', safe_date):
#         x[datetime.fromtimestamp(int(row[1])).date()] = float(row[0])

#     conn.close()
#     return x


# def create_sales_chart(currency, start_date, end_date):
#     if 0 > (to_date(end_date) - to_date(start_date)).days:
#         print('Invalid arguments, please try again')
#     else:
#         fig, ax = plt.subplots()

#         sales_dict = get_sales(to_date(start_date), to_date(end_date))
#         currency_dict = get_currency(to_date(start_date), to_date(end_date))

#         ax.plot(sales_dict.keys(), sales_dict.values(), label='PLN')

#         for key in sales_dict.keys():
#             sales_dict[key] *= currency_dict[key]

#         ax.plot(sales_dict.keys(), sales_dict.values(), label='USD')

#         ax.xaxis_date()
#         fig.autofmt_xdate()
#         plt.xlabel('Data')
#         plt.ylabel('Wartosc sprzedarzy [PLN]')
#         plt.legend()
#         plt.savefig('sales.eps')
#         plt.show()


# fill_currency(['USD', 'EUR'], '2006-01-01', '2010-01-01')
update_sales_stats()


