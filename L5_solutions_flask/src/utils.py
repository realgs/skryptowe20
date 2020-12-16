import sqlite3
from datetime import datetime

from etc.conf import PATH_TO_DB

DATE_FORMAT = "%Y-%m-%d"
USD_ISO_CODE = 'USD'
USD_EX_RATES_TABLE_NAME = 'USDPrices'
SALES_TABLE_NAME = 'Sales'

DATA_DATE_RANGE_START = datetime(2013, 1, 1)
DATA_DATE_RANGE_END = datetime(2014, 12, 31)

HOME_INFO = f"<h1>Northwind Sales API</h1><p>API for obtaining USD and PLN daily exchange rates and sales data from Northwind database in USD and PLN. Data is available for date range: {DATA_DATE_RANGE_START.strftime(DATE_FORMAT)} - {DATA_DATE_RANGE_END.strftime(DATE_FORMAT)}</p>"

ABORT_OUT_OF_RANGE_MSG = f"No data found. Note that data is available only for date range: {DATA_DATE_RANGE_START.strftime(DATE_FORMAT)} - {DATA_DATE_RANGE_END.strftime(DATE_FORMAT)}"
ABORT_END_BEFORE_START_MSG = "End date cannot be earlier than start date."
ABORT_INCORRECT_DATE_FORMAT = f"Incorrect date format: {{date}}. Required date format: {DATE_FORMAT}"


def get_db_connection(database_path=PATH_TO_DB):
    return sqlite3.connect(database_path)
