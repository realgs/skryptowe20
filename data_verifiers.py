import constans
from datetime import datetime


def to_datetime(date):
    return datetime.strptime(date, constans.DATE_FORMAT).date()


def date_format_ok(date):
    try:
        to_datetime(date)
        return True
    except ValueError:
        return False


def dates_order_ok(start_date, end_date):
    return to_datetime(start_date) < to_datetime(end_date)


def db_contains_year(date):
    return str(to_datetime(date).year) in constans.DB_YEARS_RANGE

