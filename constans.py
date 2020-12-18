import datetime as dt
from collections import namedtuple


def to_datetime(date_to_parse):
    return dt.datetime.strptime(str(date_to_parse), '%Y-%m-%d').date()


DB_NAME = 'data.db'

CACHE_UPDATE_INTERVAL = 12

APPLICATION_REQUEST_LIMIT = ['300 per day', '40 per minute']
REQUEST_LIMIT_RATE = '300 per day;40 per minute'
REQUEST_LIMIT_SALE = '200 per day;30 per minute'

DATE_FORMAT = "%Y-%m-%d"
END_DATE = to_datetime("2005-05-05")
START_DATE = to_datetime("2003-05-05")

ReturnCode = namedtuple('RETURN_CODE', ['code', 'message'])

WRONG_DATE_FORMAT = ReturnCode(400, 'Wrong date format provided, correct format is YYYYY-MM-DD')
WRONG_DATE_RANGE = ReturnCode(416, "Date out of valid range, valid range is {} to {}".format(START_DATE, END_DATE))
NO_DATA_FOUND = ReturnCode(404, "No data found for given date")
WRONG_DATE_ORDER = ReturnCode(406, "Provided dates in wrong order")
OK = ReturnCode(200, "OK")
