import requests
import psycopg2

def zad1(currency_code: str, last_days: int) -> (float, (list, list)):
    request_url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/last/{last_days}/?format=json"

    response = requests.get(request_url)

    if (response.status_code == 200):
        response_json = response.json()
        currency_rates = response_json["rates"]

        result_map = list(map(lambda c: c["mid"], currency_rates))

        return sum(result_map)/len(result_map)

    else:
        print("Unexpected response code")


def zad2() -> (float, float):
    half_a_year = 365//2
    return (zad1("USD", half_a_year), zad1("EUR", half_a_year))


def zad4():
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

        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(version)

    except (Exception, psycopg2.Error) as ex:
        print("Error while connecting to PostgreSQL", ex)
    finally:
        if (connection):
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
    zad4()


