import sqlite3
from datetime import datetime

from conf import PATH_TO_DB

DATE_FORMAT = "%Y-%m-%d"
USD_ISO_CODE = 'USD'

DATA_DATE_RANGE_START = datetime(2013, 1, 1)
DATA_DATE_RANGE_END = datetime(2014, 12, 31)


def get_db_connection(database_path=PATH_TO_DB):
    return sqlite3.connect(database_path)
