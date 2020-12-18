from constans import *


def check_date(date_string):
    try:
        date = to_datetime(date_string)
    except ValueError:
        return WRONG_DATE_FORMAT

    if date < START_DATE or date > END_DATE:
        return WRONG_DATE_RANGE

    return OK


def check_dates(date_start, date_end):
    try:
        date_from = to_datetime(date_start)
        date_to = to_datetime(date_end)
    except ValueError:
        return WRONG_DATE_FORMAT

    if date_from < START_DATE or date_from > END_DATE or date_to < START_DATE or date_to > END_DATE:
        return WRONG_DATE_RANGE

    if date_from > date_to:
        return WRONG_DATE_ORDER

    return OK
