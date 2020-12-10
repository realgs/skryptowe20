import datetime

DATE_FORMAT = "%Y-%m-%d"

def validate_date(date_text):
    try:
        if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False
    
def is_date_order_correct(date_one, date_two):
    if datetime.datetime.strptime(date_one, "%Y-%m-%d") > datetime.datetime.strptime(date_two, "%Y-%m-%d"):
        return False
    return True

def get_dates_range(start_date, end_date):
    end = datetime.datetime.strptime(end_date, DATE_FORMAT)
    start = datetime.datetime.strptime(start_date, DATE_FORMAT)
    delta = end - start
    dates = []
    for i in range(delta.days + 1):
        dates.append((start + datetime.timedelta(days=i)).strftime(DATE_FORMAT))
    return dates