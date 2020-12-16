import constans
from datetime import datetime


def date_format_ok(date):
    try:
        datetime.strptime(date, constans.DATE_FORMAT)
        return True
    except ValueError:
        return False


def db_contains_year(date):
    year = str(datetime.strptime(date, constans.DATE_FORMAT).year)
    return year in constans.DB_YEARS_RANGE

