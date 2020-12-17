import os
from datetime import datetime

CSV_FILE = '../database.csv'
CSV_DATE_FORMAT = "%m/%d/%Y"

DATE_FORMAT = "%Y-%m-%d"

DATABASE_FILENAME = '../salesData.db'
CALC_DATABASE_FILENAME = os.path.normpath(os.path.join(os.path.dirname(__file__), DATABASE_FILENAME))

NBP_API_REQUEST_MAX_COUNT = 255

DATE_RANGE_START = datetime(2013, 1, 1)
DATE_RANGE_END = datetime(2016, 12, 31)

HOME_INFO = f"<p>API for obtaining sales data from sample database in USD and PLN. " \
            f"Available date range: </br>" \
            f"{DATE_RANGE_START.strftime(DATE_FORMAT)} - {DATE_RANGE_END.strftime(DATE_FORMAT)}</p> "

OUT_OF_RANGE_MSG = f"No data found for that range.Data is available only for range: " \
                         f"{DATE_RANGE_START.strftime(DATE_FORMAT)} - {DATE_RANGE_END.strftime(DATE_FORMAT)} "
END_BEFORE_START_MSG = "Start date after end date"
INCORRECT_DATE_FORMAT = f"Incorrect date format: {{date}}. Required date format: {DATE_FORMAT}"

REQUEST_TIME_LIMIT = "10/s"
CACHE_TIMEOUT = 100

