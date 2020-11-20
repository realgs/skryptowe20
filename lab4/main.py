import requests
import psycopg2
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_currency_for_period(currency_code: str, start_date: date, end_date: date) -> [(str, float)]:
    request_url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{start_date}/{end_date}/"

    response = requests.get(request_url)

    if (response.status_code == 200):
        response_json = response.json()
        currency_rates = response_json["rates"]

        results_map = list(map(lambda x: (x['effectiveDate'], x['mid']), currency_rates))
        return results_map

    else:
        print(f"Unexpected response code: {response.status_code}")


def zad4_fill_empty_records(currencies_for_period: [(str, float)], start_date: date, end_date: date) -> [(date, float)]:
    delta = end_date - start_date
    dates_range = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

    results = []
    last_currency_value = 4.0  # In case if the first row has no currency value and we can't take previous one

    for i in range(len(dates_range)):
        current_date = dates_range[i]

        current_currency = list(filter(lambda x: x[0] == str(current_date), currencies_for_period))
        current_currency_value = last_currency_value if len(current_currency) == 0 else current_currency[0][1]

        if len(current_currency) == 0:
            results.append((current_date, last_currency_value))
        else:
            results.append((current_date, current_currency[0][1]))
            last_currency_value = current_currency_value

    return results


def zad1(currency_code: str, last_days: int) -> [(float, (list, list))]:
    request_url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/last/{last_days}/?format=json"

    response = requests.get(request_url)

    if (response.status_code == 200):
        response_json = response.json()
        currency_rates = response_json["rates"]

        result_map = list(map(lambda c: c["mid"], currency_rates))

        return sum(result_map) / len(result_map)

    else:
        print(f"Unexpected response code: {response.status_code}")


def zad2() -> (float, float):
    half_a_year = 365 // 2
    return (zad1("USD", half_a_year), zad1("EUR", half_a_year))


def zad4(currencies: [(date, float)]):
    connection_params = None

    try:
        file = open("ConnectionString.txt")
        connection_params = list(map(lambda x: x[x.index("=") + 1:], file.read().split(',')))
    except (Exception, FileNotFoundError):
        print("Could not find ConnectionString.txt")

    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user=connection_params[0],
                                      password=connection_params[1],
                                      host=connection_params[2],
                                      port=connection_params[3],
                                      database=connection_params[4])

        cursor = connection.cursor()

        create_table_script = """
        DO $$
        BEGIN
            CREATE TABLE IF NOT EXISTS purchasing.pln_currencies
            (
                id                 serial          primary key,
                currency_date      timestamp       not null,
                currency_value     numeric(8, 4)   not null
            );
        END
        $$;
        """

        insert_values_script = "INSERT INTO purchasing.pln_currencies(currency_date, currency_value) VALUES(%s, %s)"

        cursor.execute(create_table_script)
        cursor.executemany(insert_values_script, currencies)

        connection.commit()

    except (Exception, psycopg2.Error) as ex:
        print("Error while connecting to PostgreSQL", ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def zad5():
    try:
        file = open("ConnectionString.txt")
        connection_params = list(map(lambda x: x[x.index("=") + 1:], file.read().split(',')))
    except (Exception, FileNotFoundError):
        print("Could not find ConnectionString.txt")

    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user=connection_params[0],
                                      password=connection_params[1],
                                      host=connection_params[2],
                                      port=connection_params[3],
                                      database=connection_params[4])

        cursor = connection.cursor()

        select_query = """
            SELECT d.duedate, SUM(d.unitprice) "USD", SUM(d.unitprice * c.currency_value) "PLN"
            FROM purchasing.purchaseorderdetail d 
            INNER JOIN purchasing.pln_currencies c ON d.duedate = c.currency_date 
            GROUP BY d.duedate
            """

        cursor.execute(select_query)
        result = cursor.fetchall()

        dates = [datetime.strptime(x[0].date().strftime("%Y/%m/%d"), "%Y/%m/%d") for x in result]
        dates = sorted(dates)

        usd_sums = [x[1] for x in result]
        pln_sums = [x[2] for x in result]

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

        plt.plot(dates, usd_sums, label="USD")
        plt.plot(dates, pln_sums, label="PLN")

        plt.xlabel('Month')
        plt.ylabel('Sum')

        plt.legend()
        plt.show()

    except (Exception, psycopg2.Error) as ex:
        print("Error while connecting to PostgreSQL", ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    # last_days = 12
    # currency_code = "USD"
    # zad1_result = zad1(currency_code, last_days)
    # print(f"Mean currency value of {currency_code} by last {last_days} days: {zad1_result}")
    #
    # zad2_result = zad2()
    # print(f"Mean currency value of USD and EUR respectively by last half of the year: {zad2_result}")

    # zad4()

    # start_date = date(2003, 10, 26)
    # end_date = date(2004, 8, 24)
    #
    # currencies_for_period = get_currency_for_period("USD", start_date, end_date)
    # fixed_currencies = zad4_fill_empty_records(currencies_for_period, start_date, end_date)
    #
    # zad4(fixed_currencies)
    zad5()