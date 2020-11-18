import time
from datetime import datetime
from copy import deepcopy
from constants import \
    MAX_DAYS, \
    MIN_DAYS, \
    DAY_IN_SEC, \
    DATE_FORMAT, \
    FETCH_DAYS_LIMIT, \
    MSG_ERROR_INVALID_DAYS

def is_days_valid(days):
    return days > MIN_DAYS and days < MAX_DAYS

def date_sec_to_string(date):
    return datetime.fromtimestamp(date).strftime(DATE_FORMAT)

def date_string_to_datetime(date):
    return datetime.strptime(date, DATE_FORMAT)

#TODO: REFACTOR!!!
def correct_inside_weekends(rates):
    output = [rates[0]]
    for i in range(1, len(rates)):
        day_before = date_string_to_datetime(rates[i - 1].effective_date)
        current_day = date_string_to_datetime(rates[i].effective_date)
        difference = (current_day - day_before).total_seconds() / DAY_IN_SEC
        for j in range(0, int(difference)):
            correct_date = current_day.timestamp() - DAY_IN_SEC * (difference - j)
            rate = deepcopy(rates[i])
            rate.effective_date = date_sec_to_string(correct_date)
            output.append(rate)

    return output

#TODO: IMPLEMENT!!!
def correct_edge_weekends(rates, start_date, end_date):
    pass

def correct_weekends(rates, start_date, end_date):
    output = correct_inside_weekends(rates)
    #output = correct_edge_weekends(output, start_date, end_date)
    return output

def convert_days_to_dates(days):
    days+=1
    if not is_days_valid(days):
        raise Exception(MSG_ERROR_INVALID_DAYS)

    end_of_period = int(round(time.time()))
    total_days = days * DAY_IN_SEC
    fetch_request_limit = FETCH_DAYS_LIMIT * DAY_IN_SEC
    output = []

    while total_days > 0:
        days_to_fetch = fetch_request_limit if total_days - fetch_request_limit > 0 else total_days
        start_of_period = end_of_period - days_to_fetch + DAY_IN_SEC
        output.append((date_sec_to_string(start_of_period), date_sec_to_string(end_of_period)))
        end_of_period = start_of_period - DAY_IN_SEC
        total_days -= days_to_fetch

    return output
