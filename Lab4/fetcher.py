import time
import requests as req
from datetime import datetime
from data import Response_A, Url
from constants import \
    MAX_DAYS, \
    MIN_DAYS, \
    DAY_IN_SEC, \
    DATE_FORMAT, \
    AVAIL_CURRENCIES, \
    MSG_ERROR_INVALID_DAYS, \
    MSG_ERROR_FAILED_TO_FETCH, \
    MSG_ERROR_INVALID_CURRENCY

def send_req(currency, dates):
    response = req.get(Url(currency, dates[0], dates[1]).get_url())
    if(response.status_code != 200):
        print("ERROR GETTING DATA!")
    else:
        return Response_A(response)

def is_currency_valid(currency):
    return currency in AVAIL_CURRENCIES

def is_days_valid(days):
    return days > MIN_DAYS and days < MIN_DAYS

def convert_days_to_dates(days):
    today_in_ms = int(round(time.time()))
    days_in_ms = days * DAY_IN_SEC
    start_date_in_ms = datetime.fromtimestamp(today_in_ms - days_in_ms)
    return (start_date_in_ms.strftime(DATE_FORMAT), datetime.now().strftime(DATE_FORMAT))

def get_avg_rates(currency, days):
    if not is_currency_valid(currency):
        print(MSG_ERROR_INVALID_CURRENCY)
    if not is_days_valid(days):
        print(MSG_ERROR_INVALID_DAYS)
    dates = convert_days_to_dates(days)
    return send_req(currency, dates).rates
