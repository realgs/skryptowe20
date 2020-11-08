from datetime import datetime, timedelta
import time
import requests
import json

API_ADDRESS = "http://api.nbp.pl/api"
DOLLAR_CODE = 'USD'
EURO_CODE = 'EUR'
DB_CONFIG_PATH = 'dbConfig.json'


def call_nbp_api_for_rates(currency_code, start_date, end_date):
    api_start_date = start_date - timedelta(days=1)
    request_start_time = time.time()
    url = f"{API_ADDRESS}/exchangerates/rates/a/{currency_code}/{api_start_date}/{end_date}"
    response = requests.get(url)
    request_operation_time = round(time.time() - request_start_time, 4)
    print(
        f"Nbp api request completed. Status code : {response.status_code}."
        f" Operation time: {request_operation_time} seconds. Url: {url}")
    return response


def process_nbp_api_response(nbp_response, start_date):
    rates = []
    previous_date = start_date - timedelta(days=1)
    for rate in nbp_response['rates']:
        date = datetime.strptime(rate['effectiveDate'], "%Y-%m-%d").date()
        price = rate['mid']
        days_delta = date - previous_date
        for i in range(days_delta.days):
            day = previous_date + timedelta(days=i + 1)
            rates.append({"date": str(day), "rate": price})
        previous_date = date
    return {"currency": nbp_response['code'], "rates": rates}


def get_currency_rates(currency_code, start_date, end_date):
    response = call_nbp_api_for_rates(currency_code, start_date, end_date)
    if response.status_code == 200:
        try:
            content_json = json.loads(response.content)
            processed_response = process_nbp_api_response(content_json, start_date)
            return processed_response, 200
        except Exception as exc:
            print(f"There was a problem while parsing exchange rates data: '{exc}' ")
        return {"error": "There was a problem while parsing exchange rates data"}, 400
    else:
        return {"error": "Currencies exchange rates data not found"}, 404


a = get_currency_rates('usd', datetime.now().date() - timedelta(days=2), datetime.now().date())
print(a)

a2 = {
    'table': 'A',
    'currency': 'dolar amerykański',
    'code': 'USD',
    'rates': [
        {'no': '217/A/NBP/2020', 'effectiveDate': '2020-11-05', 'mid': 3.8353},
        {'no': '218/A/NBP/2020', 'effectiveDate': '2020-11-06', 'mid': 3.8194}
    ]
}
