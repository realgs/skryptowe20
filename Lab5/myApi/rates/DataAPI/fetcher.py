import requests as req
from rates.DataAPI.web_data import RatesWrapper, Url
from rates.DataAPI.date_parser import convert_days_to_dates, correct_weekends
# from constants import \
# from web_data import RatesWrapper, Url
# from date_parser import convert_days_to_dates, convert_days_to_dates_days, correct_weekends
from rates.DataAPI.constants import \
    AVAIL_CURRENCIES, \
    MSG_ERROR_FAILED_TO_FETCH, \
    MSG_ERROR_INVALID_CURRENCY

def validate_response(response):
    if(response.status_code != 200):
        raise Exception(f"{MSG_ERROR_FAILED_TO_FETCH}\n"
                        f"Status: {response.status_code}")

def send_req(currency, start_date, end_date):
    url = Url(currency, start_date, end_date)
    response = req.get(url)
    validate_response(response)
    return response

def validate_currency(currency):
    if not currency in AVAIL_CURRENCIES:
        raise Exception(MSG_ERROR_INVALID_CURRENCY)

def get_avg_rates_for_currency_days(currency, days):
    periods_to_fetch = convert_days_to_dates_days(days)
    return get_avg_rates(currency, periods_to_fetch)

def get_avg_rates_for_currency(currency, start_date, end_date):
    periods_to_fetch = convert_days_to_dates(start_date, end_date)
    return get_avg_rates(currency, periods_to_fetch)

def get_avg_rates(currency, periods_to_fetch):
    wrapper = RatesWrapper(currency, periods_to_fetch[0][0],
                           periods_to_fetch[len(periods_to_fetch)-1][1])

    for start_date, end_date in periods_to_fetch:
        response = send_req(currency, start_date, end_date)
        wrapper.append_from_response(response)

    return correct_weekends(wrapper)

def get_avg_rates_for_currencies(currencies, days):
    output = []
    for currency in currencies:
        validate_currency(currency)
        output.append(get_avg_rates_for_currency_days(currency, days))

    return output

print(get_avg_rates_for_currency('USD', '2020-12-01', '2020-12-11'))
