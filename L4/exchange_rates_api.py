import requests
import json
import datetime

MAX_DAYS_IN_ONE_REQ = 255
LINK_START = "http://api.nbp.pl/api/exchangerates/rates/a/"
LINK_END = "/?format=json"
STATUS_CODE_SUCCESS = 200
NUBER_OF_CAND_FOR_FIRST_DAY = 7


def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def get_exchange_rates_helper(first_day, last_day, currency_code):
    resp = requests.get(LINK_START + currency_code + "/" + str(first_day) + "/" + str(last_day) + LINK_END)
    exchange_rates_dict = {}
    if resp.status_code == STATUS_CODE_SUCCESS:
        exchange_rates_dict = {str_to_date(item["effectiveDate"]) : item["mid"] for item in resp.json()["rates"]}
    return exchange_rates_dict
    

def get_exchange_rates_from_to(first_day, last_day, currency_code):
    exchange_rates_dict = {}
    while (last_day - first_day).days > MAX_DAYS_IN_ONE_REQ:
        req_last_day = first_day + datetime.timedelta(days = MAX_DAYS_IN_ONE_REQ)
        exchange_rates_temp = get_exchange_rates_helper(first_day, req_last_day, currency_code)
        exchange_rates_dict.update(exchange_rates_temp)
        first_day = req_last_day

    exchange_rates_temp = get_exchange_rates_helper(first_day, last_day, currency_code)
    exchange_rates_dict.update(exchange_rates_temp)
    
    return exchange_rates_dict


def get_exchange_rates_from_last_days(days, currency_code):
    today = datetime.date.today()
    first_day = today - datetime.timedelta(days = days-1)
    return get_exchange_rates_from_to(first_day, today, currency_code)


def complete_exchange_rates(first_day, last_day, exchange_rates_dict, currency_code):
    if (first_day) not in exchange_rates_dict:
        first_day_rate = None
        candidates_for_first_day = get_exchange_rates_from_to(first_day - datetime.timedelta(days = NUBER_OF_CAND_FOR_FIRST_DAY),
            first_day - datetime.timedelta(days = 1), currency_code)
        if candidates_for_first_day == {}:
            return {}
        else:
            day_counter = 1
            while first_day_rate == None and day_counter <= NUBER_OF_CAND_FOR_FIRST_DAY:
                if (first_day - datetime.timedelta(day_counter)) in candidates_for_first_day:
                    first_day_rate = candidates_for_first_day[(first_day - datetime.timedelta(day_counter))]
                day_counter += 1
        if first_day_rate == None:
            return {}
        else:
            exchange_rates_dict.update({(first_day): first_day_rate})

    day_temp = first_day
    day_temp_rate = exchange_rates_dict[day_temp]
    while day_temp < last_day:
        day_temp += datetime.timedelta(days = 1)
        if day_temp not in exchange_rates_dict:
            exchange_rates_dict[day_temp]=day_temp_rate
        else:
            day_temp_rate = exchange_rates_dict[day_temp]

    return exchange_rates_dict
