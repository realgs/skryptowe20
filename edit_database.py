import psycopg2
import requests
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates


def generate_start_end_dates(start_date, number_of_years):
    days_in_leap_year = lambda x: 366 if ((x % 4 == 0 and x % 100 != 0) or x % 400) == 0 else 365
    start_end_dates = []
    for i in range(number_of_years):
        start_end_dates.append(start_date)
        start_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(
            days=days_in_leap_year(int(start_date[0:4])))).strftime('%Y-%m-%d')
    return start_end_dates


API_URL = "http://api.nbp.pl/api"
CURRENCY1 = 'USD'
CURRENCY2 = 'PLN'
START_END_DATES = generate_start_end_dates('2015-01-01', 4)
DEFAULT_CURRENCY = 'USD'


def get_multiple_years_data():
    rates_list = []
    for i in range(len(START_END_DATES) - 1):
        rates_list = rates_list + get_exchangerates(START_END_DATES[i], START_END_DATES[i + 1], DEFAULT_CURRENCY)
    return rates_list


def get_exchangerates(start_day, end_day, currency):
    get_currency_url = f'{API_URL}/exchangerates/rates/a/{currency}/{start_day}/{end_day}'
    stock = requests.get(get_currency_url)
    if stock.status_code != 200:
        print(f'Request error: {stock.status_code}')
        return stock.status_code
    else:
        return stock.json()['rates']


def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="pythonLab",
            user="postgres",
            password="postgres")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def create_table(conn):
    sql_create_table = '''
        CREATE TABLE IF NOT EXISTS ExchangeRates (
        rateDate date,
        rate double precision)
        '''
    cur = conn.cursor()
    cur.execute(sql_create_table)
    cur.close()
    conn.commit()


def fill_table_with_data(dates, rates, conn):
    values_to_insert = ''
    for i in range(len(dates)):
        values_to_insert += f"('{dates[i]}', {rates[i]}), "
    values_to_insert = values_to_insert[0:len(values_to_insert) - 2]

    cur = conn.cursor()
    cur.execute("INSERT INTO exchangerates VALUES %s" % values_to_insert)
    conn.commit()
    cur.close()


def fill_gaps_in_dates(dates_and_rates):
    filled_dates = []
    rates = []
    for i in range(len(dates_and_rates) - 1):
        next_day = datetime.strptime(dates_and_rates[i + 1]['effectiveDate'], '%Y-%m-%d')
        curr_day = datetime.strptime(dates_and_rates[i]['effectiveDate'], '%Y-%m-%d')
        if next_day - curr_day > timedelta(days=1):
            temp_date = curr_day
            while temp_date < next_day:
                filled_dates.append(temp_date.strftime('%Y-%m-%d'))
                rates.append(dates_and_rates[i]['mid'])
                temp_date = temp_date + timedelta(days=1)
        else:
            filled_dates.append(dates_and_rates[i]['effectiveDate'])
            rates.append(dates_and_rates[i]['mid'])
    return filled_dates, rates


def get_data_during_6moths(conn):
    sql_select_data = '''
SELECT bought, ROUND(AVG(averageprice * totalvolume)::numeric, 2) as totalValue, ROUND(AVG(averageprice * totalvolume * rate)::numeric, 2) as totalValuePLN
FROM 
    (
    SELECT * from pythonLab 
    where bought >= (SELECT MAX(bought) FROM pythonLab) - 182
    ORDER BY bought
    ) as last6Months
INNER JOIN exchangerates ON bought = ratedate
GROUP BY bought 
ORDER BY bought
'''
    cur = conn.cursor()
    cur.execute(sql_select_data)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def execute_inserting_values(conn):
    dates, rates = fill_gaps_in_dates(get_multiple_years_data())
    fill_table_with_data(dates, rates, conn)


def partition_data_to_lists(data_fetched):
    dates = []
    total_value = []
    total_value_pln = []
    for i in range(len(data_fetched)):
        dates.append(matplotlib.dates.date2num(data_fetched[i][0]))
        total_value.append(data_fetched[i][1])
        total_value_pln.append(data_fetched[i][2])
    return dates, total_value, total_value_pln


if __name__ == '__main__':
    connection = connect_to_database()
    create_table(connection)
    # execute_inserting_values()
    time_period, total_value_usd, total_value_pln = partition_data_to_lists(get_data_during_6moths(connection))
    plt.plot_date(time_period, total_value_usd, '-', linestyle='solid', xdate=True, label=CURRENCY1, figure=plt.figure(figsize=(9, 6)))
    plt.plot_date(time_period, total_value_pln, '-', xdate=True, label=CURRENCY2)
    plt.xlabel('Date')
    plt.ylabel('Value of avocados sold')
    plt.title('Total value of avocados sold during 6 mothns')
    plt.legend()
    plt.savefig('avocados_sold.svg')
    plt.show()
