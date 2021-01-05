from datetime import datetime, timedelta
import time
import requests
import json
import logging

API_ADDRESS = "http://api.nbp.pl/api"


def call_nbp_api_for_rates(currency_code, start_date, end_date):
    api_start_date = start_date - timedelta(days=5)
    request_start_time = time.time()
    url = f"{API_ADDRESS}/exchangerates/rates/a/{currency_code}/{api_start_date}/{end_date}"
    response = requests.get(url)
    request_operation_time = round(time.time() - request_start_time, 4)
    logging.info(
        f"Nbp api request completed. Status code : {response.status_code}."
        f" Operation time: {request_operation_time} seconds. Url: {url}")
    return response


def process_nbp_api_response(nbp_response, start_date, end_date):
    rates = []
    if len(nbp_response['rates']) > 0:
        previous_date = start_date
        previous_rate = nbp_response['rates'][0]
        for rate in nbp_response['rates']:
            date = datetime.strptime(rate['effectiveDate'], "%Y-%m-%d").date()
            days_delta = (date - previous_date).days
            for i in range(days_delta - 1):
                day = previous_date + timedelta(days=i + 1)
                if start_date <= day:
                    rates.append({"date": day, "rate": previous_rate, "interpolated": True})
            if start_date <= date:
                rates.append({"date": date, "rate": rate['mid'], "interpolated": False})
            previous_date = date
            previous_rate = rate['mid']
        days_delta = (end_date - previous_date).days
        for i in range(days_delta):
            day = previous_date + timedelta(days=i + 1)
            if day >= start_date:
                rate = previous_rate
                rates.append({"date": day, "rate": rate, "interpolated": True})
    return {"currencyCode": nbp_response['code'], "rates": rates}


def get_currency_rates(currency_code, start_date, end_date):
    response = call_nbp_api_for_rates(currency_code, start_date, end_date)
    if response.status_code == 200:
        try:
            content_json = json.loads(response.content)
            processed_response = process_nbp_api_response(content_json, start_date, end_date)
            return processed_response
        except Exception as exc:
            raise Exception(f"There was a problem while parsing exchange rates data: '{exc}' .")
    else:
        raise Exception(f"Currencies exchange rates data not found in NBP api.")
