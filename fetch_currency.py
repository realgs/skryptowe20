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


def get_previous_days(currency, days):
    if currency in Currency._value2member_map_ and 0 < days < 367:
        current_date = datetime.now()
        beginning = current_date - timedelta(days=days)
        response = requests.get(
            f'http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{beginning.date()}/{current_date.date()}/?format=json')
        if(response.status_code != 200):
            print(f'Request Error {response.status_code}')
            return response.status_code
        else:
            return response


def get_range(currency, start_date, end_date):
    if currency not in Currency._value2member_map_ or not 0 < (end_date - start_date).days < 367:
        print('Invalid arguments, please try again')
    else:
        response = requests.get(
            f'http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date.date()}/{end_date.date()}/?format=json')
        if(response.status_code != 200):
            print(f'Request Error {response.status_code}')
            return response.status_code
        else:
            return response


def parse_response(response):
    y = []
    x = []
    print(response.json()['rates'][1])
    for value in response.json()['rates']:
        y.append(value['mid'])
        x.append(to_date(value['effectiveDate']))
    return x, y


def create_currency_chart(currencies, days):
    if not isinstance(currencies, list) or days < 1:
        print('Invalid arguments, please try again')
    else:
        fig, ax = plt.subplots()

        for currency in currencies:
            response = get_previous_days(currency, days)
            if isinstance(response, int) or response is None:
                print(f'Failed fetching {currency}')
            else:
                x, y = parse_response(response)
                ax.plot(x, y, label=currency)

        ax.xaxis_date()
        fig.autofmt_xdate()
        plt.xlabel('Data')
        plt.ylabel('Wartosc waluty [PLN]')
        plt.legend()
        plt.savefig('currencies.eps')
        plt.show()


def fix_response(response):
    x = []
    y = []
    previous_date = response.json()['rates'][0]
    for value in response.json()['rates']:
        for date in range(1, (to_date(value['effectiveDate']) - to_date(previous_date['effectiveDate'])).days):
            y.append(previous_date['mid'])
            x.append(to_date(previous_date['effectiveDate']) + timedelta(days=date))
        y.append(value['mid'])
        x.append(to_date(value['effectiveDate']))
        previous_date = value

    return x, y


def to_date(date):
    if isinstance(date, datetime):
        return date
    else:
        return datetime.strptime(date, '%Y-%m-%d')


def fill_currency(currency, start_date, end_date):
    dates = split_date(start_date, end_date)
    x = []
    y = []
    for date_range in dates:
        response = get_range(currency, date_range[0], date_range[1])
        if isinstance(response, int) or response is None:
            print(f'Failed fetching data between {date_range[0]} and {date_range[1]}')
        else:
            fixed_data = fix_response(response)
            x.append(fixed_data[0])
            y.append(fixed_data[1])

    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    print("Opened database successfully")
    x = [item for lst in x for item in lst]
    y = [item for lst in y for item in lst]
    print(x[0])
    for date, value in zip(x, y):
        safe_data = (date.timestamp(), value,)
        c.execute('INSERT INTO currency VALUES(?,?)', safe_data)

    conn.commit()
    conn.close()


def split_date(start_date, end_date):
    days_between = (to_date(end_date) - to_date(start_date)).days
    print(days_between)
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


def get_sales(start_date, end_date):
    if (to_date(end_date) - to_date(start_date)).days < 0:
        print('Illegal argument')
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    print("Opened database successfully")
    x = {}
    previous_sales = 0

    safe_date = (to_date(start_date).timestamp(), to_date(end_date).timestamp(),)
    for row in c.execute('''SELECT SUM(SALES), ORDERDATE FROM SALES
                            WHERE ORDERDATE between ? and ?
                            GROUP BY ORDERDATE
                            ORDER BY ORDERDATE''', safe_date):
        x[datetime.fromtimestamp(int(row[1])).date()] = x.get(
            datetime.fromtimestamp(int(row[1])).date(), 0) + float(row[0])

    for key in x.keys():
        x[key] += previous_sales
        previous_sales = x[key]

    conn.close()
    return x


def get_currency(start_date, end_date):
    if (to_date(end_date) - to_date(start_date)).days < 0:
        print('Illegal argument')
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    print("Opened database successfully")
    x = {}

    safe_date = (to_date(start_date).timestamp(), to_date(end_date).timestamp(),)
    for row in c.execute('SELECT value, date from currency where date between ? and ? ORDER BY date', safe_date):
        x[datetime.fromtimestamp(int(row[1])).date()] = float(row[0])

    conn.close()
    return x


def create_sales_chart(currency, start_date, end_date):
    if 0 > (to_date(end_date) - to_date(start_date)).days:
        print('Invalid arguments, please try again')
    else:
        fig, ax = plt.subplots()

        sales_dict = get_sales(to_date(start_date), to_date(end_date))
        currency_dict = get_currency(to_date(start_date), to_date(end_date))

        ax.plot(sales_dict.keys(), sales_dict.values(), label='PLN')

        for key in sales_dict.keys():
            sales_dict[key] *= currency_dict[key]

        ax.plot(sales_dict.keys(), sales_dict.values(), label='USD')

        ax.xaxis_date()
        fig.autofmt_xdate()
        plt.xlabel('Data')
        plt.ylabel('Wartosc sprzedarzy [PLN]')
        plt.legend()
        plt.savefig('sales.eps')
        plt.show()


create_currency_chart(['USD', 'EUR'], 180)
create_sales_chart('USD', '2005-01-01', '2006-01-01')
