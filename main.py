import requests
from datetime import date, timedelta, datetime
from matplotlib import ticker, pyplot, dates
from db_handler import *


CURRENCIES_SYMBOLS = [
    'usd',
    'pln',
    'chf',
    'eur',
    'gbp'
]

REQUEST_ADDRESS = 'http://api.nbp.pl/api/exchangerates/rates/a'
REQUEST_DAYS_LIMIT = 368
PLOTS_PATH = 'plots'
PLOT_FORMAT = 'svg'
PLOTS_DAYS_RANGE = 182


def to_datetime(date_to_parse):
    return datetime.strptime(str(date_to_parse), '%Y-%m-%d').date()


def get_nearest_rate(currency, known_date):
    currency_symbol = currency.lower()
    req_date = to_datetime(known_date)
    if currency_symbol in CURRENCIES_SYMBOLS:
        while True:
            resp = requests.get(
                f'{REQUEST_ADDRESS}/{currency_symbol}/{req_date}')
            if resp.status_code == 200:
                return resp.json()
            else:
                req_date -= timedelta(days=1)


def make_request(currency, start_date, end_date):
    resp = requests.get(
        f'{REQUEST_ADDRESS}/{currency}/{start_date}/{end_date}/')
    if resp.status_code != 200:
        print(f'Request error: {resp.status_code}')
        return resp.status_code
    else:
        return process_response(resp.json(), start_date, end_date)


def process_response(response, start, end):
    first_rate_date = response['rates'][0]['effectiveDate']
    first_rate = response['rates'][0]['mid']
    last_rate_date = response['rates'][len(response['rates']) - 1]['effectiveDate']
    last_rate = response['rates'][len(response['rates']) - 1]['mid']

    days = []
    rates = []

    if start != first_rate_date:
        days_diff = (to_datetime(first_rate_date) - to_datetime(start)).days
        nearest_rate = get_nearest_rate(response['code'], start)
        for i in range(days_diff):
            days.append(str(to_datetime(start) + timedelta(days=i)))
            rates.append(nearest_rate['rates'][0]['mid'])

    days.append(first_rate_date)
    rates.append(first_rate)

    for item in response['rates'][1:]:
        prev_date = to_datetime(first_rate_date)
        days_diff = (to_datetime(item['effectiveDate']) - prev_date).days
        if days_diff > 1:
            for i in range(days_diff - 1):
                days.append(str(prev_date + timedelta(days=i + 1)))
                rates.append(first_rate)

        first_rate_date = item['effectiveDate']
        first_rate = item['mid']
        days.append(first_rate_date)
        rates.append(first_rate)

    if end != last_rate_date:
        days_diff = (to_datetime(end) - to_datetime(last_rate_date)).days
        for i in range(days_diff):
            days.append(str(to_datetime(last_rate_date) + timedelta(days=i + 1)))
            rates.append(last_rate)

    return days, rates


def split_request(currency, number_of_days, start_date):
    total_days = []
    total_rates = []
    start_date = to_datetime(start_date)
    number_of_requests, days_left = int(number_of_days / REQUEST_DAYS_LIMIT), number_of_days % REQUEST_DAYS_LIMIT
    end_date = start_date + timedelta(days=REQUEST_DAYS_LIMIT - 1)
    for i in range(number_of_requests):
        days, rates = make_request(currency, start_date, end_date)
        total_days.extend(days)
        total_rates.extend(rates)
        start_date += timedelta(days=REQUEST_DAYS_LIMIT)
        end_date += timedelta(days=REQUEST_DAYS_LIMIT)

    if days_left != 0:
        x1, y1 = make_request(currency, start_date, start_date + timedelta(days=days_left))
        total_days.extend(x1)
        total_rates.extend(y1)

    return total_days, total_rates


def get_rates_days(currency, number_of_days):
    currency_symbol = currency.lower()
    if currency_symbol in CURRENCIES_SYMBOLS:
        end_date = date.today()
        start_date = end_date - timedelta(days=number_of_days)
        if number_of_days < REQUEST_DAYS_LIMIT:
            return make_request(currency_symbol, start_date, end_date)
        else:
            return split_request(currency_symbol, number_of_days, start_date)
    else:
        print(f'Could not get data for currency: {currency_symbol}. Wrong currency symbol')


def get_rates_range(currency, start_date, end_date):
    currency_symbol = currency.lower()
    if currency_symbol in CURRENCIES_SYMBOLS:
        number_of_days = (to_datetime(end_date) - to_datetime(start_date)).days
        if number_of_days < REQUEST_DAYS_LIMIT:
            return make_request(currency, start_date, end_date)
        else:
            return split_request(currency, number_of_days, start_date)
    else:
        print(f'Could not get data for currency: {currency_symbol}. Wrong currency symbol')


def draw_two_curr_plot(currencies, days, save=True):
    fig, ax = pyplot.subplots()
    for curr in currencies:
        x, y = get_rates_days(curr, days)
        ax.plot(x, y, label=curr.upper())

    ax.xaxis.set_major_locator(dates.DayLocator(interval=8))
    ax.xaxis.set_minor_locator(dates.DayLocator(interval=1))

    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))

    fig.autofmt_xdate()
    fig.set_size_inches(15, 10)
    pyplot.grid(True)
    pyplot.title(f'Kurs {currencies[0].upper()} oraz {currencies[1].upper()} w ciągu ostatnich 6 miesięcy')
    pyplot.xlabel('Data YYYY-MM-DD')
    pyplot.ylabel('Wartość [zł]')
    pyplot.legend(loc='upper left')
    if save:
        pyplot.savefig(f'{PLOTS_PATH}/{currencies[0]}_{currencies[1]}.{PLOT_FORMAT}')
    pyplot.show()


def draw_sales_plot(currency, start_date, end_date, save=True):
    fig, ax = pyplot.subplots()

    rates_days = []
    usd_values = []
    pln_values = []

    x1, _ = get_rates_range(currency, start_date, end_date)
    res = get_sums_and_rates_for_dates(x1)
    for i in res:
        rates_days.append(i[0])
        usd_values.append(i[1])
        pln_values.append(i[1] * i[2])

    ax.plot(rates_days, usd_values, label='USD')
    ax.plot(rates_days, pln_values, label='PLN')
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))

    ax.yaxis.set_major_locator(ticker.MultipleLocator(10000))

    fig.autofmt_xdate()
    fig.set_size_inches(15, 10)
    pyplot.grid(True)
    pyplot.title('Wartości sprzedaży wyrażone w PLN i USD w półrocznym przedziale')
    pyplot.xlabel('Data YYYY-MM-DD')
    pyplot.ylabel('Wartość')
    pyplot.legend(loc='upper left')
    if save:
        pyplot.savefig(f'{PLOTS_PATH}/half_year_sales.{PLOT_FORMAT}')
    pyplot.show()


def modify_database(values):
    create_rates_table()
    insert_csv_data()
    insert_values_to_rates_table(values)


def main():
    draw_two_curr_plot(['usd', 'gbp'], PLOTS_DAYS_RANGE)
    # dates_to_db, rates_to_db = get_rates_range('usd', '2003-01-01', '2004-12-31')
    # modify_database(zip(dates_to_db, rates_to_db))

    sales_starting_date = get_first_sale_date()[0][0]
    ending_date = to_datetime(sales_starting_date) + timedelta(days=PLOTS_DAYS_RANGE)

    draw_sales_plot('usd', sales_starting_date, str(ending_date))


if __name__ == '__main__':
    main()
