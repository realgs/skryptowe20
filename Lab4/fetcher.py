import requests as req
from web_data import Response_A, Url
from date_parser import convert_days_to_dates, correct_weekends
from constants import \
    AVAIL_CURRENCIES, \
    MSG_ERROR_FAILED_TO_FETCH, \
    MSG_ERROR_INVALID_CURRENCY

def send_req(currency, dates):
    url = Url(currency, dates[0], dates[1])
    response = req.get(url)
    if(response.status_code != 200):
        raise Exception(f"{MSG_ERROR_FAILED_TO_FETCH}\nStatus: {response.status_code}")
    else:
        return Response_A(response)

def is_currency_valid(currency):
    return currency in AVAIL_CURRENCIES

def get_avg_rates(currency, days):
    if not is_currency_valid(currency):
        raise Exception(MSG_ERROR_INVALID_CURRENCY)

    pairs_of_dates = convert_days_to_dates(days)
    output = []
    for pair in pairs_of_dates:
        rates = send_req(currency, pair).rates
        for r in rates:
            output.append(r)

    output.sort(key=lambda x: x.effective_date)
    return correct_weekends(output, "", "")
