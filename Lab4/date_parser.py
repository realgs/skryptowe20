import time
from datetime import datetime
from constants import \
    MAX_DAYS, \
    MIN_DAYS, \
    DAY_IN_SEC, \
    DATE_FORMAT, \
    FETCH_DAYS_LIMIT, \
    MSG_ERROR_INVALID_DAYS

def is_days_valid(days):
    return days > MIN_DAYS and days < MAX_DAYS

def date_ms_to_string(date):
    return datetime.fromtimestamp(date).strftime(DATE_FORMAT)

def convert_days_to_dates(days):
    days+=1
    if not is_days_valid(days):
        print(MSG_ERROR_INVALID_DAYS)
    end_date = int(round(time.time()))
    total_days = days * DAY_IN_SEC
    fetch_ms = FETCH_DAYS_LIMIT * DAY_IN_SEC
    output = []

    while total_days > 0:
        days_diff = fetch_ms if total_days - fetch_ms > 0 else total_days
        start_date = end_date - days_diff + DAY_IN_SEC
        output.append((date_ms_to_string(start_date), date_ms_to_string(end_date)))
        end_date = start_date - DAY_IN_SEC
        total_days -= days_diff

    return output
