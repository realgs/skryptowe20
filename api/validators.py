import datetime
from api.constants import REQUEST_DAYS_LIMIT, DATE_FORMAT

def validate_date(date_text):
    if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
        return False
    return True
    
def is_date_order_correct(date_one, date_two):
    if datetime.datetime.strptime(date_one, "%Y-%m-%d") > datetime.datetime.strptime(date_two, "%Y-%m-%d"):
        return False
    return True

def dates_range_exceeded(start_date, end_date):
    end = datetime.datetime.strptime(end_date, DATE_FORMAT)
    start = datetime.datetime.strptime(start_date, DATE_FORMAT)
    delta = end - start
    return delta.days > REQUEST_DAYS_LIMIT

def get_dates_range(start_date, end_date):
    end = datetime.datetime.strptime(end_date, DATE_FORMAT)
    start = datetime.datetime.strptime(start_date, DATE_FORMAT)
    delta = end - start
    dates = []
    for i in range(delta.days + 1):
        dates.append((start + datetime.timedelta(days=i)).strftime(DATE_FORMAT))
    return dates
