import requests
import psycopg2
from datetime import date, timedelta, datetime
#
import flask
from currency_controller import currency_controller
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

    except (Exception, psycopg2.Error) as ex:
        print("Error while connecting to PostgreSQL", ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


##
app = flask.Flask(__name__)
app.config["DEBUG"] = True

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "300 per hour"]
)
limiter.limit("5/minute")(currency_controller)

app.register_blueprint(currency_controller)

@app.errorhandler(404)
def page_not_found(e):
    return ("Sorry but requested route was not found", 404)

if __name__ == "__main__":
    app.run()
