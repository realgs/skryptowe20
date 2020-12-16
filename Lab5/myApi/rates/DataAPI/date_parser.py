import time
from datetime import datetime, timedelta
from copy import deepcopy
# from constants import \
from rates.DataAPI.constants import \
    MAX_DAYS, \
    MIN_DAYS, \
    DAY_IN_SEC, \
    DATE_FORMAT, \
    FETCH_DAYS_LIMIT, \
    MSG_ERROR_INVALID_DAYS

def is_days_valid(days):
    return days > MIN_DAYS and days < MAX_DAYS

#TODO: implement correct logic
def are_dates_valid(start_date, end_date):
    return True

def date_sec_to_string(date):
    return datetime.fromtimestamp(date).strftime(DATE_FORMAT)

def datetime_to_string(date):
    return date.strftime(DATE_FORMAT)

def date_string_to_datetime(date):
    return datetime.strptime(date, DATE_FORMAT)

def correct_inner_weekends(rates_wrapper):
    rates = rates_wrapper.rates
    output = [rates[0]]
    for i in range(1, len(rates)):
        day_before = date_string_to_datetime(rates[i - 1].date)
        current_day = date_string_to_datetime(rates[i].date)
        difference = (current_day - day_before).total_seconds() / DAY_IN_SEC
        for j in range(0, int(difference)):
            correct_date = current_day.timestamp() - DAY_IN_SEC * (difference - (j + 1))
            rate = deepcopy(rates[i])
            rate.date = date_sec_to_string(correct_date)
            output.append(rate)

    rates_wrapper.rates = output
    return rates_wrapper

def correct_start_edge_weekend(rates_wrapper):
    start_rate = rates_wrapper.rates[0]
    if rates_wrapper.start_date < start_rate.date:
        date = date_string_to_datetime(deepcopy(rates_wrapper.start_date))
        start_rate = date_string_to_datetime(deepcopy(start_rate.date))
        for i in range(7 - date.weekday()):
            rates_wrapper.append_single_rate(datetime_to_string(date), start_rate.value)
            date += timedelta(days=1)

    return rates_wrapper

def correct_end_edge_weekend(rates_wrapper):
    end_rate = rates_wrapper.rates[len(rates_wrapper.rates) - 1]
    if rates_wrapper.end_date > end_rate.date:
        date = date_string_to_datetime(deepcopy(rates_wrapper.end_date))
        end_date = date_string_to_datetime(deepcopy(end_rate.date))
        for i in range(date.weekday() - end_date.weekday()):
            end_date += timedelta(days=1)
            rates_wrapper.append_single_rate(datetime_to_string(end_date), end_rate.value)

    return rates_wrapper

def correct_weekends(rates_wrapper):
    output = correct_inner_weekends(rates_wrapper)
    output = correct_start_edge_weekend(rates_wrapper)
    output = correct_end_edge_weekend(rates_wrapper)

    return output

def convert_days_to_dates_days(days):
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

def convert_days_to_dates(start_date, end_date):
    converted_start_date = date_string_to_datetime(start_date)
    converted_end_date = date_string_to_datetime(end_date)

    days = int((converted_end_date - converted_start_date).total_seconds() / DAY_IN_SEC)

    days+=1
    if not (is_days_valid(days) and are_dates_valid(start_date, end_date)):
        raise Exception(MSG_ERROR_INVALID_DAYS)

    end_of_period = int(round(converted_end_date.timestamp()))
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
