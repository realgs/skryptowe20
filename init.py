import requests
import sqlite3
import constants
from datetime import datetime, timedelta


def make_request(currency, start_date, end_date):
    if currency not in constants.Currency._value2member_map_ \
            or not 0 < (end_date - start_date).days <= constants.REQUEST_LIMIT:
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


def fix_response(currencies, start_date, end_date, currency):
    x = []
    if currencies[0][0] != to_date(start_date):
        request = make_request(currency, to_date(start_date) - timedelta(days=7), to_date(start_date))
        if request is not None:

            x.append((to_date(request.json()['rates'][-1]['effectiveDate']), request.json()['rates'][-1]['mid'], True))
            previous_date = x[0]
    else:
        previous_date = currencies[0]
    for value in currencies:
        for date in range(1, (to_date(value[0]) - to_date(previous_date[0])).days):
            x.append((to_date(previous_date[0]) + timedelta(days=date), previous_date[1], True))
        previous_date = value
    if currencies[-1][0] != to_date(end_date):
        for date in range(1, (to_date(end_date) - currencies[-1][0]).days + 1):
            x.append((to_date(currencies[-1][0]) + timedelta(days=date), currencies[-1][1], True))
    return x + currencies


def get_currency(currency, start_date, end_date):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''SELECT * FROM CURRENCY WHERE SYMBOL = ?
            AND DATE BETWEEN ? AND ?''', currency.upper(), start_date(), end_date())
    return c.fetchall()


def migrate_sales_stats():
    conn = sqlite3.connect('sales.db')
    conn_django = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c_django = conn_django.cursor()
    duplicates = 0
    for row in c.execute('''SELECT SUM(SALES), ORDERDATE FROM SALES
                            GROUP BY ORDERDATE
                            ORDER BY ORDERDATE'''):
        try:
            safe_data = (datetime.fromtimestamp(int(row[1])).date(), float(row[0]))
            c_django.execute('INSERT INTO sales_salesstats(date, sales_sum) VALUES(?, ?)', safe_data)
        except(sqlite3.IntegrityError):
            duplicates += 1

    print(f'{duplicates} values were already in database')
    conn.close()
    conn_django.commit()
    conn_django.close()


def get_range(currency, start_date, end_date):
    dates = split_date(start_date, end_date)
    x = []
    for date_range in dates:
        response = make_request(currency, date_range[0], date_range[1])
        if isinstance(response, int) or response is None:
            print(f'Failed fetching data between {date_range[0]} and {date_range[1]}')
        else:
            for value in response.json()['rates']:
                x.append((to_date(value['effectiveDate']), value['mid'], False))
    return fix_response(x, start_date, end_date, currency)


def split_date(start_date, end_date):
    days_between = (to_date(end_date) - to_date(start_date)).days
    dates = []
    while days_between != 0:
        if days_between >= constants.REQUEST_LIMIT:
            dates.append((to_date(end_date) - timedelta(days=days_between), to_date(end_date) -
                          timedelta(days=days_between) + timedelta(days=constants.REQUEST_LIMIT - 1)))
            days_between -= constants.REQUEST_LIMIT
        else:
            dates.append((to_date(end_date) - timedelta(days=days_between), to_date(end_date)))
            days_between = 0
    return dates


def fill_currency(currencies, start_date, end_date):
    for currency in currencies:
        currencyValues = get_range(currency, start_date, end_date)
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        print("Opened database successfully")
        duplicates = 0
        for daily_value in currencyValues:
            try:
                safe_data = (currency.upper(), daily_value[0].date(), daily_value[1], daily_value[2], )
                c.execute('INSERT INTO sales_currency(symbol,date,value,interpolated) VALUES(?,?,?,?)', safe_data)
            except sqlite3.IntegrityError:
                duplicates += 1

        if duplicates != 0:
            print(f'{duplicates} values were not added to database due to Integrity Error')
        conn.commit()
        conn.close()


fill_currency(list(map(lambda c: c.value, constants.Currency)), constants.FIRST_DAY, constants.LAST_DAY)
migrate_sales_stats()
