import requests


def zad1(currency_code: str, last_days: int) -> float:
    request_url = "http://api.nbp.pl/api/exchangerates/rates/a/{0}/last/{1}/?format=json"\
        .replace("{0}", currency_code)\
        .replace("{1}", str(last_days))

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

if __name__ == "__main__":
    last_days = 12
    currency_code = "USD"
    zad1_result = zad1(currency_code, last_days)
    print(f"Mean currency value of {currency_code} by last {last_days} days: {zad1_result}")

    zad2_result = zad2()
    print(f"Mean currency value of USD and EUR respectively by last half of the year: {zad2_result}")
