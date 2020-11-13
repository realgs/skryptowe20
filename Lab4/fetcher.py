import requests as req
from web_data import Response_A, Url
from date_parser import convert_days_to_dates
from constants import \
    AVAIL_CURRENCIES, \
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

def get_avg_rates(currency, days):
    if not is_currency_valid(currency):
        print(MSG_ERROR_INVALID_CURRENCY)

    pairs_of_dates = convert_days_to_dates(days)
    output = []
    for pair in pairs_of_dates:
        output.append(send_req(currency, pair).rates)
    return output
