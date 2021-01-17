import requests
from datetime import date, timedelta

# Min and max ranges available in the DB. TODO get range using SQL query
MIN_ALLOWED_DATE = date(2003, 10, 26)
MAX_ALLOWED_DATE = date(2004, 8, 24)

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


def fill_empty_records(currencies_for_period: [(str, float)], start_date: date, end_date: date) -> [(date, float, bool)]:
    delta = end_date - start_date
    dates_range = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

    results = []
    last_currency_value = 4.0  # In case if the first row has no currency value and we can't take previous one

    for i in range(len(dates_range)):
        current_date = dates_range[i]

        current_currency = list(filter(lambda x: x[0] == str(current_date), currencies_for_period))
        current_currency_value = last_currency_value if len(current_currency) == 0 else current_currency[0][1]

        if len(current_currency) == 0:
            results.append((current_date, last_currency_value, True))
        else:
            results.append((current_date, current_currency[0][1], False))
            last_currency_value = current_currency_value

    return results